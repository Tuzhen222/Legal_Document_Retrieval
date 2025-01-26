# Legal Document Retrieval System

## Overview
This project was developed for the SOICT Legal Document Retrieval Challenge, focusing on building an efficient and accurate system for retrieving Vietnamese legal documents based on semantic similarity. Our team achieved a Top 8 position in SoICT Hackathon 2024.

## Project Description

### Topic
The Legal Document Retrieval Challenge focuses on solving the problem of querying Vietnamese legal document data, with an emphasis on semantic understanding and accurate retrieval.

### Task
The competition centers on a single task: developing an efficient retrieval system for Vietnamese legal documents.

### Data
The competition data provided by the organizers includes three sets:
* Training data: 119,456 labeled query-document pairs for model training
* Public test: 10,000 queries for model evaluation
* Private test: 50,000 queries for final evaluation

All datasets share a common repository of legal documents.

### Evaluation Metric
The system performance is evaluated using MRR@10 (Mean Reciprocal Rank at 10), which represents the system's ability to find relevant documents in the shared document repository. See the Evaluation section for details.

## Technical Approach
Our solution combines multiple advanced techniques:
* BM25 for initial document retrieval
* Bi-encoder for semantic encoding
* Cross-encoder for result reranking
* Data chunking for efficient text processing

## Model Checkpoints

### BM25 Model
Download the BM25 model checkpoint:
```bash
pip install gdown
gdown "1VFT7UiMXgoJzGKqWxId4LORq9v0VcW7T" -O bm25/bm25_model.pkl
```

### Fine-tuned Language Model
Access our fine-tuned BGE-M3 model:
* Model: [Quintu/bge-m3-legal_retrieval](https://huggingface.co/Quintu/bge-m3-legal_retrieval)

## Dataset Setup
Download the dataset:
```bash
pip install gdown
gdown --folder 1LO4wmj54lWgQvYiGKKAUSLSv5ypMjcDA
```

## Performance
Our team achieved a Top 8 position using the combined approach of BM25, bi-encoder, and cross-encoder reranking with data chunking techniques.

## Video

Watch our project report video here: Project Report [Project Report Video](https://www.youtube.com/watch?v=7NmFXgzTgr8)