import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_excel('saavu2.xlsx')
df.columns = df.columns.str.lower()

df = df[(df['lat'] != 0) & (df['long'] != 0)]
df = df.dropna(subset=['lat','long','sales'])

X = df[['lat','long']].values
weights = df['sales'].values

kmeans = KMeans(n_clusters=20, random_state=42, n_init=50)
kmeans.fit(X, sample_weight=weights)

centroids = kmeans.cluster_centers_

pd.DataFrame(centroids, columns=['lat','long']).to_excel(
    'candidate_dcs.xlsx', index=False
)

print("Candidate DCs created")