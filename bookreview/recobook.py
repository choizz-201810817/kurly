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
bestRdf = (rdf.groupby('ISBN')['Book-Rating'].sum()>100).to_frame()
bestRdf.columns=['OK']
# %%
mdf = pd.merge(rdf, bestRdf[bestRdf['OK']==True], how='inner', on='ISBN')
mdf
# rdf.describe()
# %%
## 중복 존재 확인
udf.duplicated().sum()

# udup = pd.DataFrame(udf.duplicated(), columns=['TF'])
# udup
# %%
## pivor table
uratedf = pd.merge(udf, mdf, how='inner', on='User-ID')
urdf = uratedf.fillna(0)
urdf
#%%
urpivot = pd.pivot(urdf,
                   index = 'User-ID',   # 행 위치에 들어갈 열 
                   columns = 'ISBN',     # 열 위치에 들어갈 열 
                   values = 'Book-Rating')  # 데이터로 사용할 열

# %%
urpivot = urpivot.fillna(0)
# %%
# 유사도 기반의 추천시스템
from sklearn.metrics.pairwise import cosine_similarity
co_matrix = cosine_similarity(urpivot)
#%%
# co_matrix.shape
codf = pd.DataFrame(co_matrix)

#%%
codf[codf.iloc[10]>0].iloc[:,8:11]

# %%
bestUser = (codf[10].sort_values(ascending=False)[1:6].index)
# %%
bestRate = rdf[rdf['User-ID'].isin(bestUser)]
recoBooks = pd.merge(bestRate, bookdf, how='inner', on='ISBN')
recoBooks
# %%
# PCA 기반의 추천
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(urpivot)


# %%
pcadf = pd.DataFrame(pca.components_.T, columns=['x', 'y'])
# %%
pcadf.plot(x='x', y='y',kind='scatter')
# %%
# ML (비지도 클러스터링)
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans.fit(pcadf)
# %%
pcadf['cluster'] = kmeans.labels_
pcadf
# %%
import seaborn as sns

sns.scatterplot(pcadf, x='x', y='y', hue='cluster')
# %%
# 지도학습 ML