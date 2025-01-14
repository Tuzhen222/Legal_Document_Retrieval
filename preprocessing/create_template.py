import json
import pandas as pd
import matplotlib.pyplot as plt

train_data = "data/train.csv"
corpus_data = "data/corpus.csv"
df = pd.read_csv(train_data)
df_cp = pd.read_csv(corpus_data)


# convert corpus
template_data = [
    {
        "Field_id": "law",
        "infor": []
    }
]

for row in df.itertuples(index=False):
    print(row.question)
    
list_text_corpus = df_cp["text"].tolist()
list_text_corpus_id = df_cp["cid"].tolist()
for text, id in zip(list_text_corpus, list_text_corpus_id):
    template_data[0]["infor"].append(
        {
            "infor_id": str(id),
            "text": text
        }
    )

with open('data/template.json', 'w', encoding='utf-8') as f:
    json.dump(template_data, f, ensure_ascii=False, indent=4)