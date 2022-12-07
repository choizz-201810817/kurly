# JDK 설치 
# https://www.oracle.com/java/technologies/downloads/#jdk19-windows
# pip install konlpy, matplotlib, seaborn

# %%
from kurlyprs.kdb import selBT, selSQL
import pandas as pd
import re
from konlpy.tag import Kkma
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#%%
rows=selBT("breview",'limit 1,2', 'review')
print(rows)


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
# SELECT A.id, substr(B.date, 0, 8) MONTH, sale, title, COUNT(rkey) CNT FROM beauty A 
# LEFT JOIN breview B ON A.pcode=B.pcode 
# WHERE A.id=93
# GROUP BY A.id, substr(B.date, 0, 8)
# ORDER BY B.date ASC

tbl = 'beauty A LEFT JOIN breview B ON A.pcode=B.pcode'
where = 'WHERE A.id=93 GROUP BY A.id, substr(B.date, 0, 8) ORDER BY B.date ASC'
cols = 'A.id, substr(B.date, 0, 8) MONTH, sale, title, COUNT(rkey) CNT '

rows=selBT(tbl, where, cols)

rdf = pd.DataFrame(rows, columns=['id', 'month', 'sale', 'title', 'COUNT'])
rdf[['month', 'COUNT']].plot()

#%%
# SELECT A.id, COUNT(rkey) CNT FROM beauty A 
# LEFT JOIN breview B ON A.pcode=B.pcode
# GROUP BY A.id
# ORDER BY CNT DESC
# LIMIT 10

sql = """SELECT A.id, COUNT(rkey) CNT FROM beauty A 
LEFT JOIN breview B ON A.pcode=B.pcode
GROUP BY A.id
ORDER BY CNT DESC
LIMIT 10"""

rows = selSQL(sql)

msql = """
SELECT substr(B.date, 0, 8) MONTH, COUNT(rkey) CNT
FROM beauty A LEFT JOIN breview B ON A.pcode=B.pcode
WHERE A.id={} GROUP BY A.id, substr(B.date, 0, 8) ORDER BY B.date ASC
"""

#%%
df = pd.DataFrame()
for r in rows:
    rows = selSQL(msql.format(r[0]))
    mdf = pd.DataFrame(rows, columns=['id', str(r[0])]).set_index('id')
    df = pd.merge(df, mdf, how='outer', left_index=True, right_index=True)
# %%
plt.figure(figsize=(15,8))
df.iloc[:-1,:].fillna(0).plot()
# %%
df

# %%
