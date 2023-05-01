from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from indexer.service import run as indexer_run
from clustering.clusteringservice import run as clustering_run
from QueryExpansion.QEService import run as qe_run

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/search", methods=['POST'])
@cross_origin()
def process_input():
    json_data = request.get_json()
    query = json_data['query']
    config = json_data['config']
    rest = json_data['rest']
    response = 'ok'
    if config == 'hits':
        response = {
            "expanded_query": "",
            "results": indexer_run(query, hits=True),
        }
    else:
        if rest == 'flat_clustering':
            response = clustering_run(query, rest)
        elif rest == 'single_link':
            response = clustering_run(query, "agglomerative_clustering_single")
        elif rest == 'complete_link':
            response = clustering_run(query, "agglomerative_clustering_complete")
        elif rest == 'rocchio_algorithm':
            response = qe_run(query,"pseudo_relevance_feedback")
        elif rest == 'associative_cluster':
            response = qe_run(query,"association_clusters")
        elif rest == 'metric_cluster':
            response = qe_run(query,"metric_clusters")
        elif rest == 'scalar_cluster':
            response = qe_run(query,"scalar_clusters")
        else:
            response = {
                "expanded_query": "",
                "results": indexer_run(query),
            }
    return {
        "result": response,
    }

if __name__ == "__main__":
    app.run(port=8081)