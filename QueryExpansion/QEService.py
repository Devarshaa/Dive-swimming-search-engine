from indexer.solr_client import search
from QueryExpansion.PseudoRelevanceFeedback import expandQuery
from QueryExpansion.AssociationClusters import expandQueryAC
from QueryExpansion.MetricClusters import expandQueryMC
from QueryExpansion.ScalarClusters import expandQuerySC

def run(query, rq_type):
    results = search(query, 30)
    expanded_query = query
    if rq_type == 'pseudo_relevance_feedback':
        expanded_query = expandQuery(query, results)
    elif rq_type == 'association_clusters':
        expanded_query = expandQueryAC(query, results)
    elif rq_type == 'metric_clusters':
        expanded_query = expandQueryMC(query, results)
    elif rq_type == 'scalar_clusters':
        expanded_query = expandQuerySC(query, results)
    results = search(expanded_query, 30)
    return (expanded_query, results)

# eq, res = run('swimming medal', 'pseudo_relevance_feedback')
# print(eq, res[0])