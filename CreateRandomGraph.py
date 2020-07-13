import random
import networkx as nx
import sys
from matplotlib import pyplot as plt
import argparse

num_plots = 100
node_number = 0
graph = nx.Graph()

for i in range(num_plots):
    node_number += 1
    graph.add_node(node_number)

node_number = 0

def get_fig():
    global node_number
    node_number += 1
    kolvo = 0
    for i in range(random.randrange(1, 5)):
        while True:
            v_for_edge = random.choice(list(graph.nodes()))
            if node_number != v_for_edge:
                break

        if graph.has_edge(node_number, v_for_edge):
            kolvo += 1
            continue
        kolvo += 1
        graph.add_edge(node_number, v_for_edge)


for i in range(num_plots):
    get_fig()
    #plt.draw()
    #plt.savefig('gif/pic%s.png' % i)

dic = {}
for i in list(graph.edges):
    dic[i[0]] = 0
    dic[i[1]] = 0

for i in list(graph.edges):
    dic[i[0]] = dic[i[0]] + 1
    dic[i[1]] = dic[i[1]] + 1

kolvo = 0
for i in dic:
    kolvo = kolvo + dic.get(i)

#print((kolvo/num_plots)/num_plots*100)
#nx.draw(graph, node_size=size*100, with_labels=True, pos=pos, node_shape='o', font_size=size/5, font_color='red')
#pos = nx.spring_layout(graph)
#nx.draw(graph, nodecolor='r', with_labels=True, pos=pos)
#plt.show()
#print(nx.degree_centrality(graph))

def WriteFile():
    f = open('text.txt', 'w')
    for index in list(graph.edges):
        f.write(', '.join(str(s) for s in index) + '\n')


