import json

# Load dữ liệu JSON từ file
with open("../data/template_chunking-new.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

# Chuyển đổi sang dạng phẳng
flattened_data = []
for item in data_list:
    for info in item["infor"]:
        flattened_data.append({
            "stt": info["stt"],
            "infor_id": info["infor_id"],
            "chunk_id": info["chunk_id"],
            "text": info["text"]
        })

# Lưu lại dữ liệu đã chuyển đổi vào file mới (nếu cần)
with open("../data/template_chunking_flat.json", "w", encoding="utf-8") as f:
    json.dump(flattened_data, f, ensure_ascii=False, indent=4)

print(flattened_data[:2])
