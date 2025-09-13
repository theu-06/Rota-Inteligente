
import pandas as pd
from sklearn.cluster import KMeans

def cluster_deliveries(deliveries_csv, k):
    df = pd.read_csv(deliveries_csv)
    X = df[["addr_x", "addr_y"]].values
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_
    return df, centers
