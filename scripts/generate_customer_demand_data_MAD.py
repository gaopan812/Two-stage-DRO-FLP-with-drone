from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def classification(xihatsp, I):
    X = xihatsp
    silhouette_scores = []
    for k in range(2, 6):  # 注意轮廓系数计算时K至少为2
        kmeans = KMeans(n_clusters=k, random_state=0, n_init='auto').fit(X)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(X, labels)
        silhouette_scores.append(silhouette_avg)
    best_K = 2 + silhouette_scores.index(max(silhouette_scores))
    kmeans = KMeans(n_clusters=best_K, random_state=0, n_init='auto').fit(X)

    # 预测每个样本的簇标签
    labels = kmeans.labels_
    unique, counts = np.unique(labels, return_counts=True)
    event_num = best_K
    mu_mad = np.empty((event_num, I))
    delta_mad = np.empty((event_num, I))
    for event in range(event_num):
        row_index = np.where(labels == event)[0]
        selected_rows = X[row_index]
        temp_mean = np.mean(selected_rows, axis=0)
        mu_mad[event] = temp_mean
        temp_abs = np.abs(selected_rows - temp_mean)
        delta_mad[event] = np.mean(temp_abs, axis=0)
    return event_num, counts, mu_mad, delta_mad

