import csv
import json

def convert_to_list(s):
    s = s.strip('[]')
    elements = s.split()  
    return [int(element) for element in elements]

with open("../data/data_preprocessing/template_chunking_flat.json", "r", encoding="utf-8") as f:
    templat_chunking_flat = json.load(f)

infor_id_to_info = {
    item["infor_id"]: {"text": item["text"], "law_id": f"law_{item['chunk_id']}"}
    for item in templat_chunking_flat
}

question_answer_list = []
with open("../data/original/train_data.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cids = convert_to_list(row["cid"])
        answers = []
        for cid in cids:
            info = infor_id_to_info.get(str(cid), {})
            if info:
                answers.append({"text": info["text"], "law_id": info["law_id"]})

        question_answer = {
            "question": row["question"],
            "answer": answers
        }
        question_answer_list.append(question_answer)

with open("question_answer.json", "w", encoding="utf-8") as f:
    json.dump(question_answer_list, f, ensure_ascii=False, indent=4)

print("Đã tạo file question_answer.json thành công.")