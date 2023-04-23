from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/search", methods=['GET','POST'])
@cross_origin()
def process_input():
    json_data = request.get_json()
    config = inp['config']
    if "clustering" in json_data:
        clustering = json_data['clustering']
    if 'query' in json_data:
        query = inp['query']
    return {
        "message": 'ok',
    }

if __name__ == "__main__":
    app.run()