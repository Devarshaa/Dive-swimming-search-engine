import json
import re

import pysolr
from flask import jsonify

from index.docs import Docs

solr = pysolr.Solr('http://localhost:8983/solr/nutch', always_commit=True, timeout=10)


def search(query, no_of_rows=20):
    return map_to_docs(solr.search(query, search_handler="/select", **{
        "wt": "json",
        "rows": no_of_rows
    }))


def map_to_docs(solr_response):
    if solr_response.hits == 0:
        return jsonify("No content found. Try modifying your query")
    else:
        docs = list()
        rank = 0
        for result in solr_response:
            rank += 1
            id = "abc"
            title = ""
            url = ""
            content = ""
            anchor = ""
            if 'id' in result:
                id = result["id"]
            if 'title' in result:
                title = result['title']
            if 'url' in result:
                url = result['url']
            if 'content' in result:
                content = result['content']
                content = content.replace("\n", " ")
                content = " ".join(re.findall("[a-zA-Z]+", content))
            if 'anchor' in result:
                anchor = result['anchor']
            doc = Docs(id, title, url, content, anchor, rank).to_json()
            docs.append(doc)
    return docs
