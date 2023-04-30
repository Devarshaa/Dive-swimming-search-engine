#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import indexer.solr_client as solr

def run(query, rq_type):
    res = solr.search(query, 30)
    res = get_clustering_response(res, rq_type)
    return res
    

def get_clustering_response(api_res, rq_type):
    precomp_cluster_res  = dict()
    if rq_type == 'flat_clustering':
        f = open('./clustering/precomputed_clusters/clustering_f.txt')
        lines = f.readlines()
        f.close()
    elif rq_type == 'agglomerative_clustering_single':
        f = open('./clustering/precomputed_clusters/clustering_hs.txt')
        lines = f.readlines()
        f.close()
    elif rq_type == 'agglomerative_clustering_complete':
        f = open('./clustering/precomputed_clusters/clustering_hc.txt')
        lines = f.readlines()
        f.close()

    for l in lines:
        # print(l)
        split_index = l.rindex(',')
        url = l[:split_index]
        cluster_id = l[split_index+1:]
        if cluster_id=='':
            cluster_id = 50
        precomp_cluster_res[url] = cluster_id

    for doc in api_res:
        url = doc["url"]
        cluster = precomp_cluster_res.get(url, "50")
        doc.update({"cluster": cluster})
        doc.update({"done": "False"})

    res = []
    curr_rank = 1
    for doc in api_res:
        if doc["done"] == "False":
            cluster = doc["cluster"]
            doc.update({"done": "True"})
            doc.update({"rank": str(curr_rank)})
            curr_rank += 1
            res.append({"title": doc["title"], "url": doc["url"],
                               "meta_info": doc["meta_info"], "rank": doc["rank"]})
            for rem_docs in api_res:
                if rem_docs["done"] == "False":
                    if rem_docs["cluster"] == cluster:
                        rem_docs.update({"done": "True"})
                        rem_docs.update({"rank": str(curr_rank)})
                        curr_rank += 1
                        res.append({"title": rem_docs["title"], "url": rem_docs["url"],
                                           "meta_info": rem_docs["meta_info"], "rank": rem_docs["rank"]})

    return {
        "expanded_query": "",
        "results": res,
    }

# print(run('swimming medals','agglomerative_clustering_single')[:5])

__all__ = ['run']