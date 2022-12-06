# JDK 설치 
# https://www.oracle.com/java/technologies/downloads/#jdk19-windows
# pip install konlpy
#%%
from kurlyprs.kdb import selBT
rows=selBT("breview",'limit 1,2', 'review')
print(rows)
# %%
import pandas as pd
import re
from konlpy.tag import Kkma
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#%%
# bow Bag of words
def makeWdict(sentence):
    kkma = Kkma()
    pos = kkma.pos(sentence)
    pocate = ['NNG','NNP','NNB','NNM','VV','VA','VCP','VCN']
    wdict = {}
    
    for po in pos:
        if (po[1] in pocate):
            print(po[0])
            if po[0] in wdict.keys():
                wdict[po[0]]+=1
            else:
                wdict[po[0]]=1
            wdf = pd.DataFrame(list(wdict.items())).set_index(0)
    
    return wdf

# %%
def reSen(sentence):    
    pattern = '[^ㄱ-힣a-zA-Z0-9 .!?]'
    return re.sub(pattern,'',sentence)

rows=selBT("breview",'limit 20', 'review')
mdf = pd.DataFrame()

for r in rows:
    sen = reSen(r[0])
    sdf = makeWdict(sen)
    print(sdf.index)
    
    # mdf = pd.concat([mdf, sdf], axis=1).fillna(0).astype('int')
    mdf = pd.merge(mdf, sdf, how='outer', left_index=True, right_index=True)
    
mdf = mdf.fillna(0)
#%%
plt.figure(figsize=(25,7))
plt.imshow(mdf.values)

# %%
