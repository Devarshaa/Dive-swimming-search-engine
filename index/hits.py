import json

import networkx as nx

hub_score_w_file_path = "../resources/precomputed/hits_hubs_scores"
authority_score_w_file_path = "../resources/precomputed/hits_authority_scores"
authority_score_r_file_path = "resources/precomputed/hits_authority_scores"


def construct_outlink_map(inlink_map):
    url_outlink_map = dict()

    for to_url in inlink_map:
        inlinks = inlink_map[to_url]
        for from_url in inlinks:
            if from_url not in url_outlink_map:
                url_outlink_map[from_url] = []
            url_outlink_map[from_url].append(to_url)
    return url_outlink_map


def construct_inlink_map():
    linkdb_inlink_file = open("../resources/dumps/linkdb_inlinks", 'r').readlines()

    url_inlink_map = dict()
    inlinks = []

    for line in linkdb_inlink_file:
        if "Inlinks" in line:
            url = line.split("\t")[0]
        elif "fromUrl" in line:
            from_url = line.split(" ")[2]
            inlinks.append(from_url)
        else:
            url_inlink_map[url] = inlinks
            inlinks = []
    return url_inlink_map


def construct_networkx_graph(url_map):
    G = nx.Graph()
    edges = list()
    for u in url_map:
        links = url_map[u]
        for v in links:
            edges.append((u, v))
    G.add_edges_from(edges)
    return G


def store_json_to_file(json, file_path):
    file = open(file_path, 'w')
    file.write(json)
    file.close()


def HITS():
    inlink_map = construct_inlink_map()
    outlink_map = construct_outlink_map(inlink_map)
    graph = construct_networkx_graph(outlink_map)

    hubs, authorities = nx.hits(graph, max_iter=1000, normalized=True)

    store_json_to_file(json.dumps(hubs), hub_score_w_file_path)
    store_json_to_file(json.dumps(authorities), authority_score_w_file_path)


def compute_hits(urls):
    authority_score_file = open(authority_score_r_file_path, 'r').read()
    authority_score_json = json.loads(authority_score_file)

    clust_inp = sorted(urls, key=lambda x: authority_score_json.get(x['url'], 0.0), reverse=True)
    return clust_inp


if __name__ == "__main__":
    HITS()
