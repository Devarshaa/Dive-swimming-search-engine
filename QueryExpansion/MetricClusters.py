from util import tokenize_and_stem
from collections import defaultdict
# from indexer.solr_client import search

def find_indices(list_to_check, item_to_find):
    return [idx for idx, value in enumerate(list_to_check) if value == item_to_find]

def findMostCorrelated(tokens, queryTerms, doc_dict):
    metrics = defaultdict(int)
    for term in set(queryTerms):
        for stem in set(tokens):
            c = 0
            for doc in doc_dict.values():
                term_count = doc.count(term)
                stem_count = doc.count(stem)
                if term_count == 0 or stem_count == 0:
                    continue
                term_list = find_indices(doc, term)
                stem_list = find_indices(doc, stem)
                for idx1 in term_list:
                    for idx2 in stem_list:
                        if idx1 != idx2:
                            c += (1/abs(idx1 - idx2))
            c /= (tokens.count(term) * tokens.count(stem))
            metrics[(term, stem)] = c
    return metrics


def expandQueryMC(query, resultSet):
    tokens = []
    doc_dict = {}
    queryStems = tokenize_and_stem(query)
    for result in resultSet:
        doc_tokens = tokenize_and_stem(result['meta_info'])
        doc_dict[result['url'][0]] = doc_tokens
        tokens.extend(doc_tokens)

    # localVocab = set(tokens)
    metrics = findMostCorrelated(tokens, queryStems, doc_dict)
    metrics = sorted(metrics.items(), key=lambda item: item[1], reverse=True)[:5]
    for item in metrics:
        if item[0][1] not in queryStems:
            query += ' ' +item[0][1]
            queryStems.append(item[0][1])
    return query

# docs = search('olympics medals', 30)
# print(docs[0])
# new = expandQueryMC('olympics medals', docs)
# print(new)
# docs1 = search(new, 30)
# print(docs1[0])