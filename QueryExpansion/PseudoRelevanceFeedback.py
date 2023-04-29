# Rocchio Algorithm for Pseudo-Relevance Feedback
from util import tokenize_and_stem
from collections import defaultdict
# from indexer.solr_client import search

def expandQuery(query, resultSet):
    beta = 0.6
    gamma = 0.2
    queryStems = tokenize_and_stem(query)
    query_vector = defaultdict(int)
    for stem in set(queryStems):
        query_vector[stem] = queryStems.count(stem)
    for result in resultSet[:20]:
        doc_tokens = tokenize_and_stem(result['meta_info'])
        for stem in set(doc_tokens):
            query_vector[stem] += (beta * doc_tokens.count(stem))
    for result in resultSet[20:]:
        doc_tokens = tokenize_and_stem(result['meta_info'])
        for stem in set(doc_tokens):
            query_vector[stem] -= (gamma * doc_tokens.count(stem))
    best = sorted(query_vector.items(), key=lambda item: item[1], reverse=True)[:5]
    for item in best:
        if item[0] not in queryStems:
            query += ' ' + item[0]

    return query

# docs = search('olympics medals', 30)
# print(docs[0])
# new = expandQuery('olympics medals', docs)
# print(new)
# docs1 = search(new, 30)
# print(docs1[0])