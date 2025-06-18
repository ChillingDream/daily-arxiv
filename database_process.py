from tqdm import tqdm
from bson.objectid import ObjectId

from exts import db

collection = db.processed_arxiv_data

batch_size = 1000
last_id = ObjectId("000000000000000000000000")  # 起始最小ObjectId

total_to_process = collection.count_documents({})
print(f"预计需要处理的文档数量：{total_to_process}")

updated_count = 0
progress_bar = tqdm(total=total_to_process, desc="清理进度", unit="条")

while True:
    docs = list(
        collection.find({"_id": {"$gt": last_id}}, sort=[("_id", 1)], limit=batch_size)
    )

    if not docs:
        break

    for doc in docs:
        title = doc["title"]
        title = " ".join(title.strip().split())
        abstract = doc["abstract"]
        abstract = " ".join(abstract.strip().split())
        collection.update_one(
            {"_id": doc["_id"]}, {"$set": {"title": title, "abstract": abstract}}
        )
        updated_count += 1
        progress_bar.update(1)

    last_id = docs[-1]["_id"]

progress_bar.close()
print(f"\n处理完成：共更新了 {updated_count} 条文档。")
