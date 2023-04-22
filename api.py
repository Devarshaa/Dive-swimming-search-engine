import pysolr
from flask import Flask, request, jsonify

from index.hits import compute_hits
from index.solr_client import search

app = Flask(__name__)


@app.get('/search')
def search_solr():
    query = "*:*"
    no_of_results = 30
    if 'query' in request.args:
        query = str(request.args['query'])

    return jsonify(search(query, no_of_results))


@app.get('/hits/search')
def search_with_hits_score():
    query = "*:*"
    no_of_results = 30
    if 'query' in request.args:
        query = str(request.args['query'])
    root_set = search(query, no_of_results)

    return jsonify(compute_hits(root_set))


app.run(port='5000')
