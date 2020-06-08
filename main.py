import sys
import argparse
import math
import time
from threading import Thread

import networkx as nx
import random
from datetime import datetime
from PyQt5.QtCore import QThread


def GenerateSmallWorld(size, rewriting, seed):
    return nx.watts_strogatz_graph(size, rewriting, 0.1, seed=seed)


def GenerateRandom(size, rewriting, seed):
    if seed != None:
        random.seed = seed

    node_number = 0
    graph = nx.Graph()

    for i in range(size):
        node_number += 1
        graph.add_node(node_number)

    def get_fig(node_number):
        kolvo = 0
        rnd = random.randrange(1, rewriting)
        for i in range(rnd):
            if len(list(graph.edges(node_number))) == rnd:
                break;

            while True:
                v_for_edge = random.choice(list(graph.nodes()))
                if node_number != v_for_edge:
                    break

            if graph.has_edge(node_number, v_for_edge):
                kolvo += 1
                continue
            kolvo += 1
            graph.add_edge(node_number, v_for_edge)

    node_number = 0
    for i in range(size):
        node_number += 1
        get_fig(node_number)

    return graph


def GenerateBarabasi(size, rewriting, seed):
    return nx.barabasi_albert_graph(size, rewriting, seed=seed)


def GenerateIntaktnost(graph):
    graphs = list(nx.connected_components(graph))
    maxGraph = nx.Graph()
    maxGraph.add_edges_from(graph.edges(graphs[0]))
    for i in range(len(graphs)):
        nowGraph = nx.Graph()
        nowGraph.add_edges_from(graph.edges(graphs[i]))
        if len(maxGraph.nodes) < len(nowGraph.nodes):
            maxGraph = nowGraph

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

    intaktnost3 = 1 - (intaktnost2 / len(graph.nodes))
    #print(intaktnost3)
    return intaktnost3


def GenerateIntaktnost2(graph):
    intaktnost1 = 0
    floy_warshall = list(nx.floyd_warshall(graph).items())
    for item in floy_warshall:
        itemList = list(item[1].items())
        for item2 in itemList:
            if item2[1] == math.inf:
                intaktnost1 += 1

    result = (1 - intaktnost1 / (len(graph.nodes) ** 2))
    # print(result)
    return result


def AttackRandom(graph):
    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            # print('Не смог развязать')
            return 0, 0

        graph.remove_node(random.choice(list(graph.nodes())))

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def AttackMax(graph):
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
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            # print('Не смог развязать')
            return 0, 0

        graph.remove_node(list_d[iteration][0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def AttackMin(graph):
    dic = {}
    for i in list(graph.edges):
        dic[i[0]] = 0
        dic[i[1]] = 0

    for i in list(graph.edges):
        dic[i[0]] = dic[i[0]] + 1
        dic[i[1]] = dic[i[1]] + 1

    list_d = list(dic.items())
    list_d.sort(key=lambda i: i[1], reverse=True)

    node = list_d.pop()

    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            # print('Не смог развязать')
            return 0, 0

        if (len(graph[node[0]]) != 0):
            pope = list(graph[node[0]]).pop()
            graph.remove_node(pope)

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def AttackCentrality(graph):
    centrality = nx.eigenvector_centrality_numpy(graph)
    centralityList = list(centrality.items())
    centralitySorted = sorted(centralityList, key=lambda i: i[1])

    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            # print('Не смог развязать')
            return 0, 0

        graph.remove_node(centralitySorted.pop()[0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def AttackCentralityEach(graph):
    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            # print('\nНе смог развязать')
            return 0, 0

        centrality = nx.eigenvector_centrality_numpy(graph)
        centralityList = list(centrality.items())
        centralitySorted = sorted(centralityList, key=lambda i: i[1])
        graph.remove_node(centralitySorted.pop()[0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            # print('Развязан, потребовалось %s' % iteration)
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


class StartProgram(Thread):
    def __init__(self, generate, attack, size, j, retry, seed):
        super().__init__()
        self.generate = generate
        self.attack = attack
        self.size = size
        self.j = j
        self.retry = retry
        self.seed = seed

    def run(self):
        intaktnost = float(0)
        iterations = 0
        errors = 0
        goodGraphs = 0
        for i in range(self.retry):
            if ((i + 1) % (retry / 5) == 0):
                print('for ' + str(self.j) + ' ' + str((i+1)/self.retry*100) + '%')

            graph = nx.Graph()
            if self.generate == 'Random':
                graph = GenerateRandom(self.size, self.j, self.seed)
            elif self.generate == 'Small world':
                graph = GenerateSmallWorld(self.size, self.j, self.seed)
            else:
                try:
                    graph = GenerateBarabasi(self.size, self.j, self.seed)
                except:
                    errors = self.retry
                    break;

            intaktnost1 = float(0)
            iterations1 = 0

            if self.attack == 'Random':
                intaktnost1, iterations1 = AttackRandom(graph)
            elif self.attack == 'Centrality':
                intaktnost1, iterations1 = AttackCentrality(graph)
            elif self.attack == 'Centrality with recalculation':
                intaktnost1, iterations1 = AttackCentralityEach(graph)
            elif self.attack == 'Max':
                intaktnost1, iterations1 = AttackMax(graph)
            else:
                intaktnost1, iterations1 = AttackMin(graph)

            if iterations1 != 0:
                goodGraphs += 1
            else:
                errors += 1

            intaktnost += intaktnost1
            iterations += iterations1

        if intaktnost == 0:
            result = ('\nСредняя интактность для ' + str(self.j) + ' = ' + str(1) + '\n'
                      + 'Среднее количество удаленных вершин для ' + str(self.j) + ' = ' + str(self.size) + '\n'
                      + 'Средний успех для ' + str(self.j) + ' = ' + str(0) + '\n'
                      + 'Errors для ' + str(self.j) + ' = ' + str(errors/self.retry) + '\n')
            print(result)
        else:
            srIntaktnost = intaktnost / goodGraphs
            srIterations = float(iterations / goodGraphs)
            srIterationsPercent = float(srIterations / self.size)
            srUspex = 1 - ((srIntaktnost * srIterations) / self.size)
            result = ('\nСредняя интактность для ' + str(self.j) + ' = ' + str(srIntaktnost) + '\n'
                      + 'Среднее количество удаленных вершин для ' + str(self.j) + ' = ' + str(srIterationsPercent) + '\n'
                      + 'Средний успех для ' + str(self.j) + ' = ' + str(srUspex) + '\n'
                      + 'Errors для ' + str(self.j) + ' = ' + str(float(errors/self.retry)) + '\n')
            print(result)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', default=500, type=int, required=False)
    parser.add_argument('-seed', default=None, type=int)
    parser.add_argument('-attack', choices=['Random', 'Centrality', 'Centrality with recalculation', 'Max', 'Min'],
                        default='Centrality with recalculation', required=False)
    parser.add_argument('-generate', choices=['Random', 'Small world', 'Barabasi'], default='Small world', required=False)
    parser.add_argument('-rewriting', default=2, type=int, required=False)
    parser.add_argument('-retry', default=100, type=int, required=False)
    return parser


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    size = namespace.size
    attack = namespace.attack
    generate = namespace.generate
    rewriting = namespace.rewriting
    seed = namespace.seed
    retry = namespace.retry

    j = 0
    start_time = datetime.now()
    threads = list()
    #while j < size:
    j += 10
    thread = StartProgram(generate, attack, size, j, retry, seed)
    threads.append(thread)
    thread.start()

    for t in threads:
        t.join()

    print(datetime.now() - start_time)