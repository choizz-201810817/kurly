# %%
# SELECT a.id,substr(b.date,0,8) month,sale,title,count(rkey) cnt from beauty a 
# left join breview b on a.pcode=b.pcode
# where a.id=93 
# group by a.id,substr(b.date,0,8)
# order by b.date asc
tbl='beauty a left join breview b on a.pcode=b.pcode'
whr='where a.id=93 group by a.id,substr(b.date,0,8) order by b.date asc'
cols='a.id,substr(b.date,0,8) month,sale,title,count(rkey) cnt'
rows=selBT(tbl,whr,cols)
rdf=pd.DataFrame(rows,columns=['id','month','sale','title','cnt'])
rdf[['month','cnt']].plot()


# %%
msql=""" 
SELECT substr(b.date,0,8) month,count(rkey) cnt from 
 beauty a left join breview b on a.pcode=b.pcode 
 where a.id={} group by substr(b.date,0,8) order by b.date asc
"""
# %%
sql=""" 
SELECT a.id,count(rkey) cnt from beauty a 
 left join breview b on a.pcode=b.pcode 
 group by a.id
 order by cnt desc
 limit 10
"""
rows=selSQL(sql)
df=pd.DataFrame()
for r in rows:
    rows=selSQL(msql.format(r[0]))
    mdf=pd.DataFrame(rows,columns=['id',str(r[0])]).set_index('id')
    df=pd.merge(df,mdf,how='outer',left_index=True,right_index=True)
# %%
df.iloc[:-1,:].fillna(0).plot()
# %%
df
# %%