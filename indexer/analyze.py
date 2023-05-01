import json
import operator

from indexer.hits import construct_outlink_map, construct_networkx_graph, hub_score_w_file_path, \
    authority_score_w_file_path


def construct_inlink_map():
    linkdb_inlink_file = open('/Users/sangeethapradeep/apache-nutch-1.19/dumps/linkdb/part-r-00000', 'r').readlines()

    url_inlink_map = dict()
    inlinks = []

    for line in linkdb_inlink_file:
        if "Inlinks" in line:
            url = line.split("\t")[0]
        elif "fromUrl" in line:
            from_url = line.split(" ")[2]
            inlinks.append(from_url)
        elif line.strip() == '':
            url_inlink_map[url] = inlinks
            inlinks = []

    return url_inlink_map


def analyze_linkdb():
    inlink_map = construct_inlink_map()
    outlink_map = construct_outlink_map(inlink_map)
    G = construct_networkx_graph(outlink_map)

    # get the number of nodes and edges
    num_edges = G.number_of_edges()

    # calculate the maximum number of in and out links
    max_in_links = max(dict(G.in_degree()).values())
    max_out_links = max(dict(G.out_degree()).values())

    # display the results
    print("Total number of nodes:", len(outlink_map))
    print("Total number of links:", num_edges)
    print("Maximum number of in links:", max_in_links)
    print("Maximum number of out links:", max_out_links)


def analyze_hits_scores():
    # load the stored hub and authority scores
    with open(hub_score_w_file_path, 'r') as f:
        hubs = json.load(f)

    with open(authority_score_w_file_path, 'r') as f:
        authorities = json.load(f)

    # sort the hubs and authorities by their scores
    sorted_hubs = sorted(hubs.items(), key=operator.itemgetter(1), reverse=True)
    sorted_authorities = sorted(authorities.items(), key=operator.itemgetter(1), reverse=True)

    # print the top 10 hubs and their scores
    # print("Top 10 Hubs:")
    # for hub in sorted_hubs[:100]:
    #     print(f"{hub[0]}: {hub[1]}")

    # print the top authority and its score
    print("Top 10 Authorities:")
    for hub in sorted_authorities[100:200]:
        print(f"{hub[0]}: {hub[1]}")


if __name__ == "__main__":
    analyze_linkdb()
    analyze_hits_scores()
