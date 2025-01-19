import pandas as pd
import json
import re
import numpy as np

def convert_to_list(s):
    s = s.strip('[]')  
    elements = re.split(r'[\,\s]+', s)  
    return [int(element) for element in elements if element.strip().isdigit()]  

csv_file = '../data/original/train.csv'  
json_file = '../data/data_preprocessing/template.json'  

csv_data = pd.read_csv(csv_file)
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

valid_ids = set()
for item in json_data:
    for infor in item.get("infor", []):
        valid_ids.add(int(infor.get("infor_id", -1)))

filtered_data = []
for _, row in csv_data.iterrows():
    cid_list = convert_to_list(row['cid'])
    if all(cid in valid_ids for cid in cid_list):
        filtered_data.append(row)

filtered_df = pd.DataFrame(filtered_data)

train_ratio = 0.7
val_ratio = 0.2

total_len = len(filtered_df)
train_end = int(total_len * train_ratio)
val_end = train_end + int(total_len * val_ratio)

shuffled_df = filtered_df.sample(frac=1, random_state=42).reset_index(drop=True)  
train_df = shuffled_df[:train_end]
val_df = shuffled_df[train_end:val_end]
test_df = shuffled_df[val_end:]

train_file = '../data/original/train_data.csv'
val_file = '../data/original/val_data.csv'
test_file = '../data/original/test_data.csv'

train_df.to_csv(train_file, index=False, encoding='utf-8')
val_df.to_csv(val_file, index=False, encoding='utf-8')
test_df.to_csv(test_file, index=False, encoding='utf-8')

print(f"Dữ liệu đã được chia và lưu vào các file: {train_file}, {val_file}, {test_file}")
