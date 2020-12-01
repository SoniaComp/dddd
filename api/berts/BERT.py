import torch

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from transformers import get_linear_schedule_with_warmup
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
import random
import time
import datetime

from api.berts import getsimilar20


# 문장 테스트

def test_sentences(device, model, tokenizer, sent1,sent2):
    #print("testsenten")
    # 평가모드로 변경
    model.eval()

    sentence = '[CLS]'+sent1+'[SEP]'+sent2+'[SEP]'
    tokenized_texts = tokenizer.tokenize(sentence)
    #print(tokenized_texts)

    MAX_LEN = 512

    input_ids = [tokenizer.convert_tokens_to_ids(tokenized_texts)]
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # 어텐션 마스크 초기화
    attention_masks = []

    # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
    # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
    for seq in input_ids:
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)

    # 데이터를 파이토치의 텐서로 변환
    inputs = torch.tensor(input_ids)
    masks = torch.tensor(attention_masks)

    # 데이터를 GPU에 넣음
    b_input_ids = inputs.to(device)
    b_input_mask = masks.to(device)
            
    # 그래디언트 계산 안함
    with torch.no_grad():     
        # Forward 수행
        outputs = model(b_input_ids, 
                        token_type_ids=None, 
                        attention_mask=b_input_mask)

    # 로스 구함
    logits = outputs[0]

    # CPU로 데이터 이동
    logits = logits.detach().cpu().numpy()

    return logits

def is_similar(device, model, tokenizer, sent1,sent2):
    #print("issimilar")
    logits = test_sentences(device, model, tokenizer, sent1, sent2)
    result = np.argmax(logits, axis=1).flatten()[0]
    return result

def USEtoBERT(device, model, tokenizer, data):
    # 기존 학습된 모델이 있는 경우
    # tokenizer로 문장을 토큰으로 분리
    #print("USEtoBERT")
    data_list = []
    for i in range(len(data)): 
        sent1  = data["similar_title"].iloc[i]
        sent2  = data["title"].iloc[i]
        a = is_similar(device, model, tokenizer, sent1,sent2)
        if a == 1:
            data_list.append(i)
    
    no_data_list = [ x for x in range(len(data)) if x not in data_list ]
    
    similar_BERT = data[["title","content","answer","panrye","percent"]].iloc[data_list]
    similar_BERT["method"] = "BERT"
    similar_USE = data[["title","content","answer","panrye","percent"]].iloc[no_data_list]
    similar_USE["method"] = "USE"
    similar = pd.concat([similar_BERT, similar_USE])
    similar = similar.drop_duplicates(["title","content","answer","panrye"])
    similar = similar.iloc[0:10, :]

    return similar

    
def get_similar(device, model, tokenizer, question, content, *category):
    #print("getsimil")
    embed_df = pd.read_pickle("api/berts/embed_df_all.pkl")
    category = list(category)
    
    similar_df_USE = getsimilar20.similar_pair(question, content, embed_df, category)
    similar = USEtoBERT(device, model, tokenizer, similar_df_USE)

    return similar
