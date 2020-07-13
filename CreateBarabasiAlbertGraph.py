import networkx as nx
import matplotlib.pyplot as plt

size = 100
graph = nx.barabasi_albert_graph(size, 5, seed=1)

pos = nx.spring_layout(graph)
nx.draw(graph, node_size=size*100, with_labels=True, pos=pos, node_shape='o', font_size=size/5, font_color='red')
plt.gcf().set_size_inches(size/5, size/5)
#plt.savefig('png.png')
plt.show()

print(nx.is_connected(graph))

f = open('text.txt', 'w')
for index in list(graph.edges):
    f.write(', '.join(str(s) for s in index) + '\n')