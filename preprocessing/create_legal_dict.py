import json

# Đọc file JSON đầu vào
with open("../data/data_preprocessing/template_chunking_flat.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo dictionary mới với key theo format "law_{chunk_id}"
legal_dict = {}
for item in data:
    chunk_id = item["chunk_id"]
    key = f"law_{chunk_id}"
    legal_dict[key] = {"text": item["text"]}

# Lưu dictionary mới vào file JSON
with open("../data/data_preprocessing/legal_dict.json", "w", encoding="utf-8") as f:
    json.dump(legal_dict, f, ensure_ascii=False, indent=4)

print("Chuyển đổi thành công và đã lưu vào legal_dict.json.")
