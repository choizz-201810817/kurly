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
#%%
from konlpy.tag import Kkma

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
import sklearn
# %%