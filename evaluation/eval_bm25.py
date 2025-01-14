import numpy as np
import csv
import pandas as pd
import json

# Bước 1: Xử lý file numpy và xuất ra file văn bản
file_path = '../retrieval/bm25/test_search_bm25.npy'  
data = np.load(file_path, allow_pickle=True)

lines = []
for array_2d in data:
    line = []
    for row in array_2d[:20]:  
        line.append(str(row[0]))  
    lines.append(" ".join(line))

output_path = 'output.txt' 
with open(output_path, 'w') as f:
    f.write("\n".join(lines))

# Bước 2: Thêm qid từ file CSV vào output.txt
csv_file = '../data/original/test_data.csv'
input_txt_file = 'output.txt'
output_txt_file = 'output_with_qid.txt'

qid_list = []
with open(csv_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        qids = row['qid'].strip('[]').split(',')
        qid_list.extend(qids) 

with open(input_txt_file, mode='r', encoding='utf-8') as infile, open(output_txt_file, mode='w', encoding='utf-8') as outfile:
    lines = infile.readlines()
    for i, line in enumerate(lines):
        qid = qid_list[i] if i < len(qid_list) else '' 
        outfile.write(f"{qid.strip()} {line}")

print(f"File đã được lưu tại {output_txt_file}")

# Bước 3: Chuyển đổi stt sang infor_id
with open('../data/data_preprocessing/template_chunking_flat.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

stt_to_infor_id = {item['stt']: item['infor_id'] for item in json_data}

with open('output_with_qid.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('output_combined_updated.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        parts = line.strip().split()
        qid = parts[0]
        updated_ids = [stt_to_infor_id.get(int(stt), stt) for stt in parts[1:]]  
        ids_str = ' '.join(map(str, updated_ids))
        f.write(f"{qid} {ids_str}\n")

print("File đã được lưu với infor_id thay vì stt.")

# Bước 4: Hàm xử lý dữ liệu và tính Precision
def convert_to_list(s):
    s = s.strip('[]') 
    elements = s.split() 
    return [int(element) for element in elements]

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df['cid'] = df['cid'].apply(convert_to_list)
    return df

def read_txt(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [list(map(int, line.split())) for line in lines]

def calculate_precision(submit, answer):
    correct_count = 0
    total_count = 0
    
    for result in submit:
        qid = result[0]
        cids = result[1:11]  
        answer_cids = answer.get(qid, [])
        
        if any(cid in answer_cids for cid in cids):
            correct_count += 1
        total_count += 1
    
    return (correct_count / total_count) * 100 if total_count > 0 else 0

def calculate_mmr10(submit, answer):
    total_reciprocal_rank = 0
    total_queries = len(submit)
    
    for result in submit:
        qid = result[0]
        cids = result[1:21]  # Chỉ xét 10 kết quả đầu tiên
        answer_cids = answer.get(qid, [])
        
        reciprocal_rank = 0
        for rank, cid in enumerate(cids, start=1):
            if cid in answer_cids:
                reciprocal_rank = 1 / rank
                break
        
        total_reciprocal_rank += reciprocal_rank
    
    return total_reciprocal_rank / total_queries if total_queries > 0 else 0

# Bước 5: Đọc dữ liệu và tính Precision@10 và MMR@10
answer_df = read_csv('../data/original/test_data.csv')
submit_data = read_txt('output_combined_updated.txt')

answer_dict = {row['qid']: row['cid'] for _, row in answer_df.iterrows()}

precision_score = calculate_precision(submit_data, answer_dict)
mmr10_score = calculate_mmr10(submit_data, answer_dict)

print(f"Precision@10: {precision_score:.2f}%")
print(f"MMR@10: {mmr10_score:.4f}")
