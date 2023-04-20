import pysolr
from flask import Flask, request, jsonify

from index.solr_client import search

app = Flask(__name__)


@app.get('/search')
def search_solr():
    query = "*:*"
    no_of_results = 30
    if 'query' in request.args:
        query = str(request.args['query'])

    return jsonify(search(query, no_of_results))


app.run(port='5001')
