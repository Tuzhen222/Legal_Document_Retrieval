import csv
import json
import string
from rank_bm25 import BM25Okapi
from underthesea import word_tokenize
from tqdm import tqdm 
import pickle


number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
chars = ["a", "b", "c", "d", "đ", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]
stop_word = number + chars + ["của", "và", "các", "có", "được", "theo", "tại", "trong", "về", 
            "hoặc", "người",  "này", "khoản", "cho", "không", "từ", "phải", 
            "ngày", "việc", "sau",  "để",  "đến", "bộ",  "với", "là", "năm", 
            "khi", "số", "trên", "khác", "đã", "thì", "thuộc", "điểm", "đồng",
            "do", "một", "bị", "vào", "lại", "ở", "nếu", "làm", "đây", 
            "như", "đó", "mà", "nơi", "”", "“"]

def remove_stopword(w):
    return w not in stop_word

def remove_punctuation(w):
    return w not in string.punctuation

def lower_case(w):
    return w.lower()

def bm25_tokenizer(text):
    tokens = word_tokenize(text)
    tokens = list(map(lower_case, tokens))
    tokens = list(filter(remove_punctuation, tokens))
    tokens = list(filter(remove_stopword, tokens))
    return tokens

with open('../data/data_preprocessing/question_answer.json', 'r', encoding='utf-8') as f:
    question_answer_data = json.load(f)

with open('../data/data_preprocessing/legal_dict.json', 'r', encoding='utf-8') as f:
    legal_dict = json.load(f)

law_texts = [entry['text'] for entry in legal_dict.values()]

tokenized_corpus = [bm25_tokenizer(text) for text in law_texts]
bm25 = BM25Okapi(tokenized_corpus)

with open('bm25_model.pkl', 'wb') as f:
    pickle.dump(bm25, f)