## 책추천
#%%
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
# %%
bbook='data\BX_Books.csv'
brate='data\BX-Book-Ratings.csv'
buser='data\BX-Users.csv'
bookdf = pd.read_csv(bbook, encoding='latin-1', sep=';')
ratedf = pd.read_csv(brate, encoding='latin-1', sep=';')
userdf = pd.read_csv(buser, encoding='latin-1', sep=';')
# %%
bookdf.tail()
#%%
bookdf.info()
# %%
udf=userdf.dropna()
udf.info()
# %%
ratedf.info()
# %%
bookdf.describe()
# %%
userdf.describe()
# %%
ratedf.describe()
# %%
## 시각화
sns.displot(udf['Age'])
# %%
sns.boxplot(x=udf['Age'], data=udf['Age'], orient='vertical')
# %%
sns.displot(bookdf[(bookdf['Year-Of-Publication']>1960) & \
    (bookdf['Year-Of-Publication']<2001)])
# %%
# ratedf[ratedf['User-ID']
#        .apply(lambda x: True if x in userdf['User-ID'].values.tolist() else False)]

rdf = ratedf[ratedf['User-ID'].isin(list(udf['User-ID']))]

# %%
rdf.describe()
# %%
## 중복 존재 확인
udf.duplicated().sum()

# udup = pd.DataFrame(udf.duplicated(), columns=['TF'])
# udup
# %%
## pivor table
uratedf = pd.merge(udf, rdf, how='left', on='User-ID')
urdf = uratedf.fillna(0)
urdf
#%%
urpivot = pd.pivot(urdf,
                   index = 'User-ID',   # 행 위치에 들어갈 열 
                   columns = 'sex',     # 열 위치에 들어갈 열 
                   values = 'age',      # 데이터로 사용할 열 
                   aggfunc = 'mean')    # 데이터 집계함수
# %%
