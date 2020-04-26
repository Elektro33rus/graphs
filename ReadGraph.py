import networkx as nx
from matplotlib import pyplot as plt
import random
import os
from sklearn.ensemble import AdaBoostClassifier

graph = nx.Graph()

dataset = '1000,60.40proc'
os.mkdir("gif/"+dataset)
f = open(dataset+'.txt')
for line in f:
    u_for_edge, v_for_edge, ves = line.split(', ')
    graph.add_edge(int(u_for_edge), int(v_for_edge))

size = len(graph.nodes)

pos = nx.spring_layout(graph, k=1)
#nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
#plt.show()

dic = {}
for i in list(graph.edges):
    dic[i[0]] = 0
    dic[i[1]] = 0

for i in list(graph.edges):
    dic[i[0]] = dic[i[0]] + 1
    dic[i[1]] = dic[i[1]] + 1

list_d = list(dic.items())
list_d.sort(key=lambda i: i[1], reverse=True)

iteration = -1
node = list_d.pop()
while True:
    iteration += 1

    if (len(graph.nodes) <= 1):
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/'+dataset+'/pic%s.png' % iteration)
        plt.close()
        print('Не смог развязать')
        break

    #graph.remove_node(random.choice(list(graph.nodes())))
    #graph.remove_node(list_d[iteration][0])
    if (len(graph[node[0]]) != 0):
        pope = list(graph[node[0]]).pop()
        graph.remove_node(pope)
    if (iteration%(size//50) == 0):
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/'+dataset+'/pic%s.png' % iteration)
        plt.close()
    if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/'+dataset+'/pic%s.png' % iteration)
        plt.close()
        print('Развязан, потребовалось %s' % iteration)
        break

    if not nx.is_connected(graph):
        graphs = list(nx.connected_components(graph))
        for i in range(len(graphs)):
            if len(graph.edges(graphs[i])) == 0:
                printgraph = nx.Graph()
                edge = graphs[i].pop()
                printgraph.add_edge(edge, edge)
                nx.draw(printgraph, nodecolor='r', with_labels=True, pos=pos)
            else:
                printgraph = nx.Graph()
                printgraph.add_edges_from(graph.edges(graphs[i]))
                nx.draw(printgraph, nodecolor='r', with_labels=True, pos=pos)
            plt.draw()
            plt.savefig('gif/'+dataset+'/ConnectionGraph%s.png' % i)
            plt.close()

        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/'+dataset+'/pic%s.png' % iteration)
        plt.close()
        print('Развязан, потребовалось %s' % iteration)
        break
