import re
import json

def split_text_keeping_sentences(text, max_word_count):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    current_word_count = 0
    
    for sentence in sentences:
        word_count = len(sentence.split())
        
        if current_word_count + word_count > max_word_count:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_word_count = word_count
        else:
            current_chunk += " " + sentence.strip() if current_chunk else sentence.strip()
            current_word_count += word_count
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def create_flat_chunks(input_file, output_file, max_words=400):
    with open(input_file, "r", encoding="utf-8") as f:
        data_template = json.load(f)
        
    flattened_output = []
    count = 0
    
    for context in data_template[0]["infor"]:
        text = context["text"]
        infor_id = context["infor_id"]
        chunks = split_text_keeping_sentences(text, max_words)
        
        for i, chunk in enumerate(chunks):
            flattened_output.append({
                "stt": count,
                "infor_id": infor_id,
                "chunk_id": f"{infor_id}_{i}",
                "text": chunk
            })
            count += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flattened_output, f, ensure_ascii=False, indent=4)
    
    return flattened_output

if __name__ == "__main__":
    input_file = "../data/data_preprocessing/template.json"
    output_file = "../data/data_preprocessing/template_chunking_flat.json"
    
    flattened_data = create_flat_chunks(input_file, output_file)
    print(f"First chunk sample: {flattened_data[0]}")