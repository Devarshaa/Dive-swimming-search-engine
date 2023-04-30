#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from time import time
from sklearn.cluster import KMeans
from collections import defaultdict
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import pandas as pd

import json
doc_list = []
url_list = []
site_content = dict()
evaluations = []
evaluations_std = []

def load_data():
    f = open('final_solr.json', encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

def tokenize(text):
    tokens = wordpunct_tokenize(text)
    return tokens

def remove_stopwords(tokens):
    english_stopwords = stopwords.words("english")
    tokens = [token for token in tokens if token not in english_stopwords]
    return tokens

def remove_special_characters(tokens):
    tokens = [token.lower() for token in tokens if token.isalnum()]
    return tokens
    
def process_data(data):
    for doc in data['response']['docs']:
        url = doc['url']
        if 'content' in doc:
            content = doc['content']
            content = doc['content']
            tokens = tokenize(content)
            tokens = remove_special_characters(tokens)
            content = ' '.join(tokens)
            if url not in site_content:
                site_content[url] = content
                url_list.append(url)
                doc_list.append(content)
                
def plotgraph(x, y):
    x = np.array(x)
    y = np.array(y)
    
    plt.plot(x,y)
    plt.show()
            
def processDataForClustering():
    vectorizer = TfidfVectorizer(max_df = 0.5, min_df = 0.1, stop_words='english')
    t0 = time()
    X_tfidf = vectorizer.fit_transform(doc_list)
    print(f"vectorization done in {time() - t0:.3f} s")
    
    lsa = make_pipeline(TruncatedSVD(n_components=100), Normalizer(copy=False))
    t0 = time()
    X_lsa = lsa.fit_transform(X_tfidf)
    explained_variance = lsa[0].explained_variance_ratio_.sum()
    print(f"LSA done in {time() - t0:.3f} s")
    
    return X_lsa
    
def getOptimalK(X_lsa):
    optimalk = 2
    sse = []
    sil = []
    kvalues = []
    for k in range(4,20):
        km = KMeans(
        n_clusters=k,
        max_iter=100,
        n_init=1,)
        km.fit(X_lsa)
        centroids = km.cluster_centers_
        pred_clusters = km.predict(X_lsa)
        curr_sse = 0
        
        for i in range(len(X_lsa)):
            curr_center = centroids[pred_clusters[i]]
            curr_sse += (X_lsa[i, 0] - curr_center[0]) ** 2 + (X_lsa[i, 1] - curr_center[1]) ** 2
            
        sse.append(curr_sse)
        sil.append(silhouette_score(X_lsa, km.labels_, metric = 'euclidean'))
        kvalues.append(k)
        
    plotgraph(kvalues, sse)
    plotgraph(kvalues, sil)

    
    


# In[2]:


data = load_data()
process_data(data)
X = processDataForClustering()
getOptimalK(X)


# In[3]:


def kmeans(X_lsa):
    t0 = time()
    km = KMeans(
        n_clusters=10,
        max_iter=100,
        n_init=1,)
    km.fit(X_lsa)
    print(f"Kmeans done in {time() - t0:.3f} s")

    # Store K-means clustering results in a file
    t0 = time()
    id_series = pd.Series(url_list)
    cluster_series = pd.Series(km.labels_)
    results = (pd.concat([id_series,cluster_series], axis=1))
    results.columns = ['id', 'cluster']
    results.to_csv("./precomputed_clusters/clustering_f.txt", sep=',', columns=['id', 'cluster'], header=False, index=False, encoding='utf-8')
    print(f"Time to store flat clustering results {time() - t0:.3f} s")

kmeans(X)


# In[ ]:





# In[ ]:





# In[ ]:




