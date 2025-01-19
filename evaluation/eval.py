import pandas as pd

import json

# with open('../data/data_preprocessing/template_chunking_flat.json', 'r', encoding='utf-8') as f:
#     json_data = json.load(f)

# # Tạo dictionary ánh xạ từ stt đến infor_id
# stt_to_infor_id = {item['stt']: item['infor_id'] for item in json_data}

# # Đọc file txt và thay thế stt bằng infor_id
# with open('../retrieval/bi_encoder/result_bge+e5.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()

# # Mở file để ghi kết quả mới
# with open('output_combined_updated.txt', 'w', encoding='utf-8') as f:
#     for line in lines:
#         parts = line.strip().split()
#         qid = parts[0]
#         updated_ids = [stt_to_infor_id.get(int(stt), stt) for stt in parts[1:]]  # thay thế stt bằng infor_id
#         ids_str = ' '.join(map(str, updated_ids))
#         f.write(f"{qid} {ids_str}\n")

# print("File đã được lưu với infor_id thay vì stt.")

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

def calculate_mrr(submit, answer):
    mrr_scores = []
    for result in submit:
        qid = result[0]  
        cids = result[1:11]  
        answer_cids = answer.get(qid, [])
        rank = None
        for i, cid in enumerate(cids):
            if cid in answer_cids:  
                rank = i + 1  
                break
        if rank: mrr_scores.append(1 / rank)
    return sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0

answer_df = read_csv('../data/original/val_data.csv') 
submit_data = read_txt('../retrieval/result/val/phase1/bge-bm25+bm25.txt')  

answer_dict = {row['qid']: row['cid'] for _, row in answer_df.iterrows()}

mrr_score = calculate_mrr(submit_data, answer_dict)
print(f"MRR@10: {mrr_score}")
