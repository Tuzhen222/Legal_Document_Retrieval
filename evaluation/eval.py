import pandas as pd

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

answer_df = read_csv('../data/original/test_data.csv') 
submit_data = read_txt('../result/test/phase1/bge+bm25.txt')  

answer_dict = {row['qid']: row['cid'] for _, row in answer_df.iterrows()}

mrr_score = calculate_mrr(submit_data, answer_dict)
print(f"MRR@10: {mrr_score}")
