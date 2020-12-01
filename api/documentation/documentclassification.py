# coding=utf8
import pandas as pd
import numpy as np
from konlpy.tag import Mecab
import joblib
import collections

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB # 다항분포 나이브 베이즈 모델

def get_tag(input_sentence):
    # print(input_sentence)
    mecab = Mecab()
    x_nouns = [" ".join(mecab.nouns(input_sentence))] # split input sentence into nouns

    mnb = joblib.load('api/documentation/MultinomialNB.pkl') # load MultinomialNB
    dtmvector = joblib.load('api/documentation/dtmvector.pkl') # load dtm matrix
    tfidf_transformer = joblib.load('api/documentation/tfidf_transformer.pkl') # load tfidf transformer

    X_test_dtm = dtmvector.transform(x_nouns)
    tfidfv_test = tfidf_transformer.transform(X_test_dtm)
    prob_array = mnb.predict_proba(tfidfv_test)[0]
    top6_idx = np.argsort(prob_array)[-6:]
    top6_idx = top6_idx[::-1]
    top6_idx = list(top6_idx)

    top6_cat = list(map(lambda x : "성범죄" if x == 0
                   else "임대차" if x == 1
                   else "계약일반" if x == 2
                   else "손해배상" if x == 3
                   else "노동/인사" if x == 4
                   else "지식재산권" if x == 5
                   else "회생/파산" if x == 6
                   else "IT/테크" if x == 7
                   else "기업일반" if x == 8
                   else "금융" if x == 9
                   else "행정" if x == 10
                   else "등기/등록" if x == 11
                   else "매매" if x == 12
                   else "세금" if x == 13
                   else "개인정보" if x == 14
                   else "문서위조" if x == 15
                   else "약식명령/즉결심판", top6_idx))

    return top6_cat