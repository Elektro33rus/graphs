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

from pprint import pprint
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

def RunTest(generate, attack, size, j, seed):
    if generate == 'Random':
        graph = GenerateRandom(size, j, seed)
    elif generate == 'Small world':
        graph = GenerateSmallWorld(size, j, seed)
    else:
        try:
            graph = GenerateBarabasi(size, j, seed)
        except:
            return 1, size, True

    if attack == 'Random':
        intaktnost, iterations = AttackRandom(graph)
    elif attack == 'Centrality':
        intaktnost, iterations = AttackCentrality(graph)
    elif attack == 'Centrality with recalculation':
        intaktnost, iterations = AttackCentralityEach(graph)
    elif attack == 'Max':
        intaktnost, iterations = AttackMax(graph)
    else:
        intaktnost, iterations = AttackMin(graph)

    error = 0
    if intaktnost == 0:
        error = 1

    iterations = iterations/size

    return intaktnost, iterations, error

def RunTest2(retry, generate, attack, size, j, seed):
    urls_list = []
    test = list()
    test.append(generate)
    test.append(attack)
    test.append(size)
    test.append(j)
    test.append(seed)
    for i in range(0, retry):
        urls_list.append(test)

    pool = ThreadPool(10)
    results = pool.starmap(RunTest, urls_list)

    intaktnosts = 0
    errors = 0
    deleted = 0
    for result in results:
        intaktnosts += result[0]
        deleted += result[1]
        errors += result[2]

    intaktnosts = intaktnosts / (retry-errors)
    deleted = deleted / (retry - errors)
    print(intaktnosts)
    print(deleted)
    print(str(1 - (intaktnosts * deleted)))
    print(errors/retry)


start_time = datetime.now()
RunTest2(100, 'Small world', 'Centrality with recalculation', 100, 10, None)
print(datetime.now() - start_time)
