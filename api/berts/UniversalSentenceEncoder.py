# @title Setup common imports and functions
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
import warnings
warnings.filterwarnings(action="ignore")


def embed_text(input_text):
    module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'  # @param ['https://tfhub.dev/google/universal-sentence-encoder-multilingual/3', 'https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3']
    model = hub.load(module_url)
    return model(input_text)


def similarity(embedded_question, embedded_data):
    # arccos based text similarity (Yang et al. 2019; Cer et al. 2019)
    sim = 1 - np.arccos(sklearn.metrics.pairwise.cosine_similarity(embedded_question, embedded_data)) / np.pi

    return sim


def topsim(question, embedded_data, category):
    # category에 해당하는 데이터셋 추출
    embedded_data['similarity'] = 0
    embedded_data = embedded_data[embedded_data["category"].isin(category)]

    # 질문 embedding
    Qembed = embed_text(question)
    embeddings = list(embedded_data['embeddings'])

    for i in range(len(embeddings)):
        sim = similarity(Qembed, embeddings[i])
        embedded_data['similarity'].iloc[i] = sim

    testset = embedded_data.sort_values(by='similarity', ascending=False)[0:20]

    return testset


def get_similar_USE(inputQ, Qlist, category):
    
    similarity_df = topsim(inputQ, Qlist, category)

    return similarity_df[['title', 'content','answer',"panrye","percent"]]


# if __name__ == "__main__":

#     # 저장된 임베딩(dataframe) pickle 파일 불러오기
#     embed_df = pd.read_pickle("./embed_df.pkl")
#     question = input("뭐가 궁금한가요?")
#     category = input("카테고리를 선택하세요")
    
#     print(get_similar_USE(question, embed_df, category))