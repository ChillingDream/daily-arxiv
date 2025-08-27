import os
import re
import shutil
import tarfile
import tempfile

import requests


def download_arxiv_source(arxiv_id: str) -> bytes:
    """
    通过 arXiv 的 e-print 接口下载源代码（tar.gz），返回二进制内容。
    """
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    try:
        resp = requests.get(url)
    except requests.RequestException as e:
        return None
    if resp.status_code != 200:
        return None
    return resp.content


def extract_tarball_to_dir(tar_bytes: bytes, extract_dir: str) -> None:
    """
    将 bytes 格式的 tar.gz 写到临时文件，然后解压到 extract_dir。
    """
    # 先把 bytes 写入一个临时文件
    os.makedirs(os.path.join("./tmp", extract_dir), exist_ok=True)
    tmp_tar_path = os.path.join(os.path.join("./tmp", extract_dir), "source.tar.gz")
    with open(tmp_tar_path, "wb") as f:
        f.write(tar_bytes)

    # 解压
    with tarfile.open(tmp_tar_path, "r:gz") as tf:
        tf.extractall(path=os.path.join("./tmp", extract_dir))

    # 删除临时 tar.gz
    os.remove(tmp_tar_path)


def find_main_tex_file(root_dir: str) -> str:
    """
    遍历 extract_dir 下所有 .tex 文件，找到第一个包含 '\\begin{document}' 的文件，返回它的绝对路径。
    如果找不到，则返回 None。
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not fname.lower().endswith(".tex"):
                continue
            full_path = os.path.join(dirpath, fname)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    # 匹配 \begin{document}，说明它是主 tex
                    if re.search(r"\\begin\{document\}", text):
                        return full_path
            except Exception:
                # 某些 .tex 文件可能存在编码问题，忽略
                continue
    return None


def inline_inputs(tex_path: str, base_dir: str, seen: set) -> str:
    """
    递归地读取 tex_path 文件，将其中所有 \input{...} 或 \include{...} 的内容“展开”
    （也就是用那个被引用的 .tex 文件的实际内容替换掉 \input{...} 这一行），
    并去除以百分号开头的注释行。返回展开后的纯文本（字符串）。

    - tex_path: 要处理的当前 .tex 文件路径
    - base_dir: 所有源文件所在的根目录（方便拼接相对路径）
    - seen: 已经展开过的文件路径集合，用来避免循环引用
    """
    # 如果已经展开过，就返回空串，避免死循环
    if tex_path in seen:
        return ""
    seen.add(tex_path)

    result_lines = []
    try:
        with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
            for raw_line in f:
                # 1) 如果整行是注释（行首可有空白、然后百分号），跳过
                if re.match(r"^\s*%+", raw_line):
                    continue

                # 2) 查找 \input{...} 或 \include{...}，并尝试展开
                #    例如：   \input{sections/introduction}
                #    对应的文件路径可能是 base_dir/sections/introduction.tex
                m = re.match(r".*\\(input|include)\{(.+?)\}", raw_line)
                if m:
                    sub_path = m.group(2).strip()
                    # 如果没有 .tex 后缀，就加上
                    if not sub_path.lower().endswith(".tex"):
                        sub_path += ".tex"

                    # 构造实际路径（相对当前文件所在目录）
                    # 例如： tex_path = /tmp/abcd/main.tex，sub_path = sections/intro.tex
                    # base = /tmp/abcd
                    current_dir = os.path.dirname(tex_path)
                    candidate = os.path.join(current_dir, sub_path)
                    # 如果该路径不存在，再尝试以 base_dir 为根寻找
                    if not os.path.isfile(candidate):
                        candidate = os.path.join(base_dir, sub_path)

                    if os.path.isfile(candidate):
                        # 递归展开
                        inlined = inline_inputs(candidate, base_dir, seen)
                        result_lines.append(inlined)
                        continue
                    # 如果找不到对应 tex，就当普通文本保留这一行
                    # （某些情况下可能引用的文件在其他子目录里，或者命名不一致，需要手动检查）
                # 3) 如果不是 input/include，直接保留这一行
                result_lines.append(raw_line)
    except Exception:
        # 读取或解析出错时，忽略该文件内容
        pass

    return "".join(result_lines)


def extract_sections_from_tex(full_tex: str) -> dict:
    """
    在展开后的完整 LaTeX 文本中，匹配 \section{...}，并提取“Introduction”、“Method(或 Methodology)”和
    “Experiments(或 Results/Evaluation)”三部分的正文。返回一个 dict：
      {
        "introduction": "...",
        "method": "...",
        "experiments": "..."
      }
    如果某个部分没匹配到，则对应值为空字符串。

    匹配策略（最简单）：按照以下关键字判断所属章节
      - Section 名中包含 “introduction” → key="introduction"
      - Section 名中包含 “method” / “methodology” / “approach” → key="method"
      - Section 名中包含 “experiment” / “result” / “evaluation” → key="experiments"

    全文里会先用正则把所有 \section{XXX} 都找出来，记录它们在字符串中的起始位置。然后把每个目标章节的范围切出来。
    """
    # 1) 去除行首注释（%）后，如果某一行发生断行或缩进导致正则漏检，可允许后面有任意空白
    tex_nocomment = []
    for line in full_tex.splitlines():
        if re.match(r"^\s*%+", line):
            continue
        tex_nocomment.append(line)
    full_tex = "\n".join(tex_nocomment)

    # 2) 去除图片环境（如果有的话）
    full_tex = re.sub(
        r"\\begin\{figure\}.*?\\end\{figure\}", "", full_tex, flags=re.DOTALL
    )
    full_tex = re.sub(
        r"\\begin\{wrapfigure\}.*?\\end\{wrapfigure\}", "", full_tex, flags=re.DOTALL
    )
    full_tex = re.sub(
        r"\\begin\{figure\*\}.*?\\end\{figure\*\}", "", full_tex, flags=re.DOTALL
    )

    # 3) 提取表格环境，以便按照引用分配的到各个section
    tables = {}
    table_pattern = re.compile(
        r"\\begin\{table\}.*?\\end\{table\}|\\begin\{table\*\}.*?\\end\{table\*\}",
        re.DOTALL,
    )
    for match in table_pattern.finditer(full_tex):
        table_content = match.group(0)
        # 使用表格的label作为 key
        label_match = re.search(r"\\label\{(.+?)\}", table_content)
        if label_match:
            label = label_match.group(1).strip()
            tables[label] = table_content
    # 从全文中删除表格内容，避免干扰节匹配
    full_tex = table_pattern.sub("", full_tex)

    # 4) 匹配所有 \section{...}（包含可选的星号形式 \section*{...}）
    sect_pattern = re.compile(r"\\section\*?\{(.+?)\}")
    matches = list(sect_pattern.finditer(full_tex))

    # 5) 先初始化输出字典
    sections = {
        "introduction": "",
        "method": "",
        "experiments": "",
        "related work": "",
        "full": full_tex,
    }

    # 辅助：把原始节名归一化到我们想要的 key
    def normalize_title(title: str) -> str:
        lt = title.strip().lower()
        if "introduction" in lt:
            return "introduction"
        if "related work" in lt:
            return "related work"
        if "method" in lt or "approach" in lt or "methodology" in lt:
            return "method"
        if "experiment" in lt or "result" in lt or "evaluation" in lt:
            return "experiments"
        return "unknown"

    # 6) 遍历 matches，把感兴趣的章节的起止点记录下来
    #    比如 matches = [ (pos1, "Introduction"), (pos2, "Related Work"), (pos3, "Method"), ... ]
    #    我们只要 pos1-pos_next，pos3-pos_next 这些区间

    for idx, m in enumerate(matches):
        raw_title = m.group(1).strip()
        key = normalize_title(raw_title)
        if key == "unknown":
            if not sections["introduction"] or sections["experiments"]:
                continue
            else:
                key = "method"

        start_pos = m.end()
        # 下一个节的 pos 或全文末尾
        if idx + 1 < len(matches):
            end_pos = matches[idx + 1].start()
        else:
            end_pos = len(full_tex)

        # 切片时保留纯文本即可，不用保留 \section{…} 这一行
        content = full_tex[start_pos:end_pos].strip()
        if idx == len(matches) - 1:
            content = content.split("\end{document}")[0].strip()  # 去掉文档末尾的内容
        # 如果已经找到过同名节，就拼接（有些论文会把 Method 拆成几节）
        if sections[key]:
            sections[key] += "\n\n" + content
        else:
            sections[key] = content

    # 7) 如果一节引用了表格，将对应表格内容添加节末尾
    for sec_key in sections:
        for label, table_content in tables.items():
            if label in sections[sec_key]:
                sections[sec_key] += "\n\n" + table_content

    return sections


def download_and_extract_tex(arxiv_id: str):
    """
    下载 arXiv 源代码，解压并提取 Introduction/Method/Experiments 章节。
    返回一个 dict，包含各章节内容。
    """
    # 1. 下载源代码 tar.gz
    tar_bytes = download_arxiv_source(arxiv_id)
    if not tar_bytes:
        return "download error"

    # 2. 解压到临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        extract_tarball_to_dir(tar_bytes, tmpdir)

        # 3. 找到主 .tex 文件
        main_tex = find_main_tex_file(tmpdir)
        if not main_tex:
            raise "main text not found"

        # 4. 展开所有 \input / \include
        full_tex = inline_inputs(main_tex, tmpdir, seen=set())

    # 5. 提取各章节
    sections = extract_sections_from_tex(full_tex)
    return sections


if __name__ == "__main__":
    sections = download_and_extract_tex("2506.02208")
    print(sections["introduction"])
    print("=" * 20)
    print(sections["method"])
    print("=" * 20)
    print(sections["experiments"])
