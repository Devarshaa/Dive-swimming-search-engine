from indexer.hits import compute_hits
from indexer.solr_client import search


def run(query, result_size=30, hits=False):
    if query is None:
        return "query cannot be null"

    page_ranked_response = search(query, no_of_rows=result_size)

    hits_response = []
    if hits:
        hits_response = compute_hits(page_ranked_response)

    return hits_response if hits else page_ranked_response
