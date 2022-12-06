# JDK 설치 
# https://www.oracle.com/java/technologies/downloads/#jdk19-windows
# pip install konlpy
#%%
from kurlyprs.kdb import selBT
rows=selBT("breview",'limit 1,2', 'review')
print(rows)
# %%
import pandas as pd
from konlpy.tag import Kkma

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
rows=selBT("breview",'limit 5', 'review')

for r in rows:
    sdf = makeWdict(r[0])
    print(sdf)
    
#%%