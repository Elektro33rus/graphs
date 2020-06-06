import math

import networkx as nx
from matplotlib import pyplot as plt
import random
import os
import shutil

graph = nx.Graph()

dataset = 'text'

path = 'gif/'+dataset
try:
    shutil.rmtree(path)
    print("Directory '%s' has been removed successfully" %path)
except OSError as error:
    print("Directory '%s' not found" %path)

os.mkdir(path)
f = open(dataset+'.txt')
for line in f:
    u_for_edge, v_for_edge = line.split(', ')
    graph.add_edge(int(u_for_edge), int(v_for_edge))

size = len(graph.nodes)

def SaveGraph(graph, path):
    nx.draw(graph, node_size=size*100, with_labels=True, pos=pos, node_shape='o', font_size=size/5, font_color='red')
    plt.gcf().set_size_inches(size/5, size/5)
    #plt.savefig(path)
    plt.close()
    print('SaveGraph')

pos = nx.spring_layout(graph, k=0.3)

dic = {}
for i in list(graph.edges):
    dic[i[0]] = 0
    dic[i[1]] = 0

for i in list(graph.edges):
    dic[i[0]] = dic[i[0]] + 1
    dic[i[1]] = dic[i[1]] + 1

list_d = list(dic.items())
list_d.sort(key=lambda i: i[1], reverse=True)

iteration = 0
node = list_d.pop()

centrality = nx.eigenvector_centrality_numpy(graph)
centralityList = list(centrality.items())
centralitySorted = sorted(centralityList, key=lambda i: i[1])

while True:
    iteration += 1

    if (len(graph.nodes) <= 1):
        SaveGraph('gif/' + dataset + '/pic%s.png' % iteration)
        print('Не смог развязать')
        break

    #graph.remove_node(random.choice(list(graph.nodes())))
    #graph.remove_node(list_d[iteration][0])
    #centrality = nx.eigenvector_centrality_numpy(graph)
    #centralityList = list(centrality.items())
    #centralitySorted = sorted(centralityList, key=lambda i: i[1])
    graph.remove_node(centralitySorted.pop()[0])
    #if (len(graph[node[0]]) != 0):
        #pope = list(graph[node[0]]).pop()
        #graph.remove_node(pope)
    if (iteration%(size//50) == 0 or iteration == 1):
        SaveGraph(graph, 'gif/'+dataset+'/pic%s.png' % iteration)
        print('Рисую')
    if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
        SaveGraph(graph, 'gif/' + dataset + '/pic%s.png' % iteration)
        print('Развязан, потребовалось %s' % iteration)
        break

    if not nx.is_connected(graph):

        intaktnost1 = 0
        graphs = list(nx.connected_components(graph))
        test = list(nx.floyd_warshall(graph).items())
        for item in test:
            itemList = list(item[1].items())
            for item2 in itemList:
                if item2[1] == math.inf:
                    intaktnost1 += 1

        print(1 - intaktnost1 / (len(graph.nodes) ** 2))
        maxGraph = nx.Graph()
        maxGraph.add_edges_from(graph.edges(graphs[0]))
        for i in range(len(graphs)):
            nowGraph = nx.Graph()
            nowGraph.add_edges_from(graph.edges(graphs[i]))
            if len(maxGraph.nodes) < len(nowGraph.nodes):
                maxGraph = nowGraph

            if len(graph.edges(graphs[i])) == 0:
                printgraph = nx.Graph()
                edge = graphs[i].pop()
                printgraph.add_edge(edge, edge)
                SaveGraph(printgraph, 'gif/'+dataset+'/ConnectionGraph%s.png' % i)
            else:
                printgraph = nx.Graph()
                printgraph.add_edges_from(graph.edges(graphs[i]))
                SaveGraph(printgraph, 'gif/'+dataset+'/ConnectionGraph%s.png' % i)

        graphs = list(nx.connected_components(graph))
        intaktnost2 = 0
        for i in range(len(graphs)):
            nowGraph = graph
            if len(graph.edges(graphs[i])) == 0:
                nowGraph = nx.Graph()
                edge = graphs[i].pop()
                nowGraph.add_edge(edge, edge)
            else:
                nowGraph = nx.Graph()
                nowGraph.add_edges_from(graph.edges(graphs[i]))

            if (nowGraph.nodes.items() != maxGraph.nodes.items()):
                intaktnost2 += len(nowGraph.nodes)

        print(1-intaktnost2/len(graph.nodes))

        SaveGraph(graph, 'gif/'+dataset+'/pic%s.png' % iteration)
        print('Развязан, потребовалось %s' % iteration)
        break
