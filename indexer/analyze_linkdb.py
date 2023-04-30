from indexer.hits import construct_outlink_map, construct_networkx_graph


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


inlink_map = construct_inlink_map()
outlink_map = construct_outlink_map(inlink_map)
G = construct_networkx_graph(outlink_map)


# add nodes and edges to the graph
# ...

# get the number of nodes and edges
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

# calculate the maximum number of in and out links
max_in_links = max(dict(G.in_degree()).values())
max_out_links = max(dict(G.out_degree()).values())

# display the results
print("Total number of nodes:", len(outlink_map))
print("Total number of links:", num_edges)
print("Maximum number of in links:", max_in_links)
print("Maximum number of out links:", max_out_links)
