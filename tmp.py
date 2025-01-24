import pandas as pd
import matplotlib.pyplot as plt

# Đọc file CSV
file_path = 'data/original/corpus.csv'  # Thay bằng đường dẫn tới file CSV của bạn
df = pd.read_csv(file_path)

# Tính độ dài của từng dòng trong cột 'text'
df['text_length'] = df['text'].astype(str).apply(lambda x: len(x.split()))

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.hist(df['text_length'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Text Lengths', fontsize=16)
plt.xlabel('Number of Words in Text', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
