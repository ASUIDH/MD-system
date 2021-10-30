import os
import networkx as nx

def getdictGraph(basePath,queryNode):
    subGraph , pos = getSubGraph(basePath,queryNode)
    nodes = [] #nodes
    links = [] #links
    for node,attr in subGraph.nodes().items():
        nodeDict = {}
        nodeDict["id"] = str(node)
        nodeDict["category"] = attr['type'] # cat本来是一个int，后续优化一下
        nodeDict["name"] = attr['name']
        nodeDict["x"] = pos[node][0] * 1000
        nodeDict["y"] = pos[node][1] * 1000
        # vaule 可能是大小
        # symbol size可能是lable大小，这些先不加
        nodes.append(nodeDict)
    for edge in subGraph.edges():
        linkDict = {}





def getSubGraph(basePath,queryNode):
    nodePath = os.path.join(basePath,"graph.node")
    edgePath = os.path.join(basePath,"graph.edge")
    name_id,id_name,id_type = getId(nodePath)
    edges = getedge(edgePath)
    G = nx.Graph()
    G.add_edges_from(edges)
    nodesSet = set()
    nodesSet.add(queryNode)
    nei1= set(G.neighbors(queryNode))
    nodesSet |= (nei1)
    nei2 = set()
    for node in nei1:
        nei2 |= set(G.neighbors(node))
    for node in nei2 :
        if id_type[node] == "pefile":
            nodesSet.add(node)
    subGraph =  G.subgraph(nodesSet)
    for node in nodesSet:
        subGraph.nodes[node]["type"] = id_type[node]
        subGraph.nodes[node]["name"] = id_name[node]
    pos = nx.drawing.spring_layout(subGraph)
    return subGraph,pos,
def getId(graphPath):
 name_id = {}
 id_name = {}
 id_type = {}
 with open(graphPath) as f:
     for line in f.readlines():
         arr = line.strip().split()
         id = int(arr[0])  # id是一个int
         type = arr[1]
         name = arr[2]
         name_id[name] = id
         id_name[id] = name
         id_type[id] = type
 return name_id, id_name,id_type
def getedge(edgePath):
    edges = []
    with open (edgePath) as f:
        for line in f.readlines():
            arr = [int(node) for  node in line.strip().split("\t")]
            edges.append(arr)
    return edges

if __name__ == "__main__" :
    g,pos = getSubGraph(
        "D:\\MD-data\\vt\\vt",
        0
    )
    for node,att in g.nodes().items():
        print(node)
        print(att)
    print(g)
    print(pos)
    print(g.edges())