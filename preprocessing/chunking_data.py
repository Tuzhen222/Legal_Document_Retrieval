import re
import json

def split_text_keeping_sentences(text, max_word_count):
    # Tách văn bản thành các câu
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    current_word_count = 0

    for sentence in sentences:
        # Đếm số từ trong câu
        word_count = len(sentence.split())
        
        # Nếu thêm câu vào chunk hiện tại sẽ vượt quá số lượng từ tối đa
        if current_word_count + word_count > max_word_count:
            # Thêm chunk hiện tại vào danh sách chunks
            chunks.append(current_chunk.strip())
            current_chunk = sentence  # Bắt đầu một chunk mới
            current_word_count = word_count  # Đặt lại số lượng từ
        else:
            current_chunk += " " + sentence.strip() if current_chunk else sentence.strip()
            current_word_count += word_count

    # Thêm chunk còn lại nếu có
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

if __name__ == "__main__":
    path_template = "../data/template.json"
    data_template = json.load(open(path_template, "r"))

    final_output = [
        {
            "Field_id": "law",
            "infor": []
        }
    ]
    count = 0
    print(len(data_template[0]["infor"]))
    for context in data_template[0]["infor"]:
        text = context["text"]
        infor_id = context["infor_id"]
        chunks = split_text_keeping_sentences(text, 400)
        for i, chunk in enumerate(chunks):
            final_output[0]["infor"].append(
                {
                    "stt": count,
                    "infor_id": infor_id,
                    "chunk_id": infor_id + "_" + str(i),
                    "text": chunk
                }
            )
            count += 1

    with open('../data/template_chunking-new.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)

        