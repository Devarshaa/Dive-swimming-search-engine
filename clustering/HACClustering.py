#!/usr/bin/env python
# coding: utf-8

# In[5]:


from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from collections import defaultdict
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import time
import fastcluster
from scipy.cluster.hierarchy import ward, dendrogram
import sys
sys.setrecursionlimit(150000)

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
    tokens = [token.lower() for token in tokens if token not in english_stopwords]
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
    t0 = time.time()
    X_tfidf = vectorizer.fit_transform(doc_list)
    print(f"vectorization done in {time.time() - t0:.3f} s")
    
    lsa = make_pipeline(TruncatedSVD(n_components=100), Normalizer(copy=False))
    t0 = time.time()
    X_lsa = lsa.fit_transform(X_tfidf)
    explained_variance = lsa[0].explained_variance_ratio_.sum()
    print(f"LSA done in {time.time() - t0:.3f} s")
    
    return X_lsa


data = load_data()
process_data(data)
X = processDataForClustering()


# In[ ]:


# Apply Hierarchical Clustering (Single link)
t0 = time.time()
agg_d = fastcluster.linkage(X, method='single', metric='euclidean')
print(f"Time taken for single linkage: {time.time() - t0:.3f} s")

t0 = time.time()
fig, ax = plt.subplots(figsize=(10, 10))
ax = dendrogram(agg_d, orientation="right", labels=url_list)
print(f"Time taken for applying hierarchical clustering: {time.time() - t0:.3f} s")


# Get labels
t0 = time.time()
for key in ax:
    if key == "ivl":
        hc_key = ax[key]
    if key == "color_list":
        hc_dict = dict([(y,x+1) for x,y in enumerate(sorted(set(ax[key])))])
        hc_value = [hc_dict[x] for x in ax[key]]
print(f"Time taken for getting labels: {time.time() - t0:.3f} s")

# Store hierarchical clustering results in a file
t0 = time.time()
hc_cluster_series = pd.Series(hc_value)
hc_id_series = pd.Series(hc_key)
hc_results = (pd.concat([hc_id_series, hc_cluster_series], axis=1))
hc_results.columns = ['id', 'cluster']
hc_results.to_csv("./precomputed_clusters/clustering_hs.txt", sep=',', columns=['id', 'cluster'], header=False, index=False, encoding='utf-8')

print(f"Time taken for storing results of single link hierarchical clustering: {time.time() - t0:.3f} s")


# In[4]:



t0 = time.time()
agg_d = fastcluster.linkage(X, method='complete', metric='euclidean')
print(f"Time taken for complete linkage: {time.time() - t0:.3f} s")

t0 = time.time()
fig, ax = plt.subplots(figsize=(10, 10))
ax = dendrogram(agg_d, orientation="right", labels=url_list)
print(f"Time taken for applying hierarchical clustering: {time.time() - t0:.3f} s")


# Get labels
t0 = time.time()
for key in ax:
    if key == "ivl":
        hc_key = ax[key]
    if key == "color_list":
        hc_dict = dict([(y,x+1) for x,y in enumerate(sorted(set(ax[key])))])
        hc_value = [hc_dict[x] for x in ax[key]]
print(f"Time taken for getting labels: {time.time() - t0:.3f} s")

# Store hierarchical clustering results in a file
t0 = time.time()
hc_cluster_series = pd.Series(hc_value)
hc_id_series = pd.Series(hc_key)
hc_results = (pd.concat([hc_id_series, hc_cluster_series], axis=1))
hc_results.columns = ['id', 'cluster']
hc_results.to_csv("./precomputed_clusters/clustering_hc.txt", sep=',', columns=['id', 'cluster'], header=False, index=False, encoding='utf-8')

print(f"Time taken for storing results of complete link hierarchical clustering: {time.time() - t0:.3f} s")


# In[ ]:





# In[ ]:





# In[ ]:




