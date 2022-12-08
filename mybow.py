# JDK 설치 
# https://www.oracle.com/java/technologies/downloads/#jdk19-windows
# pip install konlpy, matplotlib, seaborn

#%%
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
from kurlyprs.kdb import selBT,selSQL
from kurlyprs.kreview import getReview, getTopReview
from konlpy.tag import Kkma

#%%

# 데이터 준비
rows=selBT("breview",'limit 1,2','review')
# 정제
def reSEN(sen):
    pattern='[^ㄱ-힣a-zA-Z0-9 .!?]'
    return re.sub(pattern,'',sen)

def makeSentence(senten):
    # 형태소 분석기 준비
    kkma=Kkma()
    pos=kkma.pos(senten) 
    pocate=['NNG','NNP','NNB','NNM','VV','VA','VCP','VCN']
    sentence=''
    wordlist=[]
    for po in pos:
        if(po[1] in pocate):
            wordlist.append(po[0])
            sentence=' '.join(wordlist)
    return sentence, wordlist

def getCorpus(rows=[]):
    corpus=[]
    cowordlist=[]
    for r in rows:
        sen=reSEN(r[0])
        sen,wlist=makeSentence(sen)
        corpus.append(sen)
        cowordlist.append(wlist)
    return corpus,cowordlist

# %%
cl,wl=getCorpus(rows)
print(cl)
print(wl)

# %%
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words=['록시땅','컬리'], ngram_range=(1,1), min_df=0)
X = cv.fit_transform(cl)
names = cv.get_feature_names_out()
cbow = X.toarray()
print("names:", names)
# print('단어 인덱스:', cv.vocabulary_)
print('cbow:', cbow)

# %%
# TF-IDF
# 모든 문장에서 빈번하게 나오는 단어는 그 가중치 값이 떨어짐.
# ngram으로 묶어서 "축구팀 못했다", "축구팀 잘했다" 와 같이 나오면 훨씬 낫다
from sklearn.feature_extraction.text import TfidfVectorizer
tv = TfidfVectorizer(stop_words=['록시땅','컬리'], ngram_range=(1,1), min_df=0)
X = tv.fit_transform(cl)
names=tv.get_feature_names_out()
tbow = X.toarray()

print('names:',names)
# print('단어 인덱스:', tv.vocabulary_)
print('tbow:', tbow)

# %%
# LDA(잠재 디리클레 할당)

#%%
import gensim
#%%
trows = getTopReview(1)
for tr in trows:
    print(tr)
    revs = getReview(tr[0])
    
revs
# %%
