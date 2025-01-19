import numpy as np
import pandas as pd
import json
import csv

file_path = '../result/test_search_bm25.npy'
data = np.load(file_path, allow_pickle=True)

lines = []
for array_2d in data:
    line = [str(row[0]) for row in array_2d[:20]]
    lines.append(" ".join(line))

csv_file = '../data/original/test_data.csv'
qid_list = []
with open(csv_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        qids = row['qid'].strip('[]').split(',')
        qid_list.extend(qids)

output_with_qid = []
for i, line in enumerate(lines):
    qid = qid_list[i] if i < len(qid_list) else ''
    output_with_qid.append(f"{qid.strip()} {line}")

with open('../data/data_preprocessing/template_chunking_flat.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

stt_to_infor_id = {item['stt']: item['infor_id'] for item in json_data}

output_combined_updated = []
for line in output_with_qid:
    parts = line.strip().split()
    qid = parts[0]
    updated_ids = [stt_to_infor_id.get(int(stt), stt) for stt in parts[1:]]
    ids_str = ' '.join(map(str, updated_ids))
    output_combined_updated.append(f"{qid} {ids_str}")

def convert_to_list(s):
    s = s.strip('[]')
    elements = s.split()
    return [int(element) for element in elements]

def read_csv_to_dict(file_path):
    df = pd.read_csv(file_path)
    df['cid'] = df['cid'].apply(convert_to_list)
    return {row['qid']: row['cid'] for _, row in df.iterrows()}

def parse_combined_results(lines):
    return [list(map(int, line.split())) for line in lines]

def calculate_precision(submit, answer):
    correct_count = 0
    total_count = 0
    
    for result in submit:
        qid = result[0]
        cids = result[1:21]
        answer_cids = answer.get(qid, [])
        
        if any(cid in answer_cids for cid in cids):
            correct_count += 1
        total_count += 1
    
    return (correct_count / total_count) * 100 if total_count > 0 else 0

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

answer_dict = read_csv_to_dict('../data/original/test_data.csv')
submit_data = parse_combined_results(output_combined_updated)

precision_score = calculate_precision(submit_data, answer_dict)
mrr10_score = calculate_mrr(submit_data, answer_dict)

print(f"Precision@10: {precision_score:.2f}%")
print(f"MRR@10: {mrr10_score:.4f}")
