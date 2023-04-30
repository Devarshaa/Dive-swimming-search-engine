from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from indexer.service import run as indexer_run

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
        response = indexer_run(query)
    else:
        if rest == 'flat_clustering' or rest == 'single_link' or rest == 'centroid':
            print("clustering")
        elif rest == 'rocchio_algorithm' or rest == 'associative_cluster' or rest == 'metric_cluster' or rest == 'scalar_cluster':
            print("query expansion")
        else:
            response = indexer_run(query, hits=False)
    return {
        "result": response,
    }

if __name__ == "__main__":
    app.run()