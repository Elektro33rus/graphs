import networkx as nx
from matplotlib import pyplot as plt
import random

graph = nx.Graph()

f = open('100,25-50proc.txt')
for line in f:
    u_for_edge, v_for_edge, ves = line.split(', ')
    graph.add_edge(int(u_for_edge), int(v_for_edge))

size = len(graph.nodes)

pos = nx.spring_layout(graph, k=1)
#nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
#plt.show()

iteration = 0
while True:
    iteration += 1

    if (len(graph.nodes) <= 1):
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.show()
        print('Не смог развязать')
        break

    graph.remove_node(random.choice(list(graph.nodes())))
    if (iteration%(size//50) == 0):
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/pic%s.png' % iteration)
        plt.close()
    if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
        print('Развязан, потребовалось %s' %iteration)
        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/pic%s.png' % iteration)
        plt.close()
        break

    if not nx.is_connected(graph):
        print('Развязан, потребовалось %s' %iteration)
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
            plt.savefig('gif/ConnectionGraph%s.png' % i)
            plt.close()

        nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
        plt.draw()
        plt.savefig('gif/pic%s.png' % iteration)
        plt.close()
        break
