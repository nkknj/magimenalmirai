import sys
import numpy as np
import pandas as pd

filename=sys.argv[1]
df=pd.read_excel(filename)
df=df.sort_values(by=["前年度ランク"], ascending=True)

rank=df[df["前年度ランク"]>=0]
temp=df[~(df["前年度ランク"]>=0)]
temp=temp.reset_index(drop=True)

K=np.zeros(temp.shape[0])
for i in range(K.shape[0]):
    K[i]=np.sum(df['チーム名']==temp['チーム名'][i])

temp['チーム内ランク']=temp['チーム内ランク']/K

temp=temp.sort_values(by=["チーム内ランク", "チームランク"], ascending=True)

rank=pd.concat([rank, temp])
rank=rank.reset_index(drop=True)
rank.index+=1

rank.to_excel('rank_'+filename)
