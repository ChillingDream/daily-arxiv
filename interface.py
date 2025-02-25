import gradio as gr

# 初始化一个空列表来存储词语
words_list = []

def add_word(new_word):
    """添加新词语到列表中."""
    if new_word and new_word not in words_list:
        words_list.append(new_word)
    return words_list

def delete_word(word_to_delete):
    """从列表中删除指定的词语."""
    if word_to_delete in words_list:
        words_list.remove(word_to_delete)
    return words_list

# 创建 Gradio 界面
with gr.Blocks() as demo:
    with gr.Tab('关键词设置'):
        with gr.Row():
            with gr.Column():
                word_input = gr.Textbox(label="输入新的词语")
                add_button = gr.Button("添加词语")

                word_to_delete_input = gr.Dropdown(label="选择要删除的词语", choices=words_list)
                delete_button = gr.Button("删除词语")

            words_display = gr.Textbox(label="当前词语列表", lines=10, interactive=False)


        # 添加词语按钮的事件处理
        add_button.click(add_word, inputs=word_input, outputs=words_display).then(
            lambda: gr.Dropdown(choices=words_list), outputs=word_to_delete_input)

        # 删除词语按钮的事件处理
        delete_button.click(delete_word, inputs=word_to_delete_input, outputs=words_display).then(
            lambda: gr.Dropdown(choices=words_list), outputs=word_to_delete_input)

demo.launch()