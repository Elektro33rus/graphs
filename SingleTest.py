import sys
import argparse
from threading import Thread
import networkx as nx
import random
from datetime import datetime

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
    graphConnections = list(nx.connected_components(graph))
    интактность = 0
    for i in range(len(graphConnections)):
        nowGraph = nx.Graph()
        nowGraph.add_edges_from(graph.edges(graphConnections[i]))
        if len(nowGraph.nodes) == 0:
            nowGraphNodes = 1
        else:
            nowGraphNodes = len(nowGraph.nodes)

        for j in range(i + 1, len(graphConnections)):
            currentGraph = nx.Graph()
            currentGraph.add_edges_from(graph.edges(graphConnections[j]))
            if len(currentGraph.nodes) == 0:
                currentGraphNodes = 1
            else:
                currentGraphNodes = len(currentGraph.nodes)
            интактность += currentGraphNodes*nowGraphNodes*2

    return 1 - интактность/(len(graph.nodes) ** 2)


def AttackClustering(graph):
    iteration = 0

    clustering = nx.square_clustering(graph)
    list_d = list(clustering.items())
    list_d.sort(key=lambda i: i[1], reverse=True)

    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        graph.remove_node(list_d[iteration][0])
        iteration += 1


def AttackRandom(graph):
    iteration = 0
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        iteration += 1

        graph.remove_node(random.choice(list(graph.nodes())))


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
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        graph.remove_node(list_d[iteration][0])
        iteration += 1


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
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if (len(graph[node[0]]) != 0):
            pope = list(graph[node[0]]).pop()
            graph.remove_node(pope)

        iteration += 1


def AttackCentrality(graph):
    centrality = nx.eigenvector_centrality_numpy(graph)
    centralityList = list(centrality.items())
    centralitySorted = sorted(centralityList, key=lambda i: i[1])

    iteration = 0
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        graph.remove_node(centralitySorted.pop()[0])
        iteration += 1


def AttackCentralityEach(graph):
    iteration = 0
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        centrality = nx.eigenvector_centrality_numpy(graph, tol=1e-03)
        centralityList = list(centrality.items())
        centralitySorted = sorted(centralityList, key=lambda i: i[1])
        graph.remove_node(centralitySorted.pop()[0])

        iteration += 1


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
        intaktnostShare = float(0)
        iterationsShare = 0
        errors = 0
        goodGraphs = 0
        for i in range(self.retry):
            if ((i + 1) % (retry / 20) == 0):
                print('for ' + str(self.j) + ' ' + str((i+1)/self.retry*100) + '%')

            if generate == 'Случайный':
                graph = GenerateRandom(self.size, self.j, self.seed)
            elif generate == 'Ватца-Строгаца':
                graph = GenerateSmallWorld(self.size, self.j, self.seed)
            elif generate == 'Барабаши-Альберт':
                graph = GenerateBarabasi(self.size, self.j, self.seed)
            else:
                return

            if attack == 'Случайная':
                intaktnost, iterations = AttackRandom(graph)
            elif attack == 'Центральность':
                intaktnost, iterations = AttackCentrality(graph)
            elif attack == 'Центральность с перерасчётом':
                intaktnost, iterations = AttackCentralityEach(graph)
            elif attack == 'Максимальная связность':
                intaktnost, iterations = AttackMax(graph)
            elif attack == 'Минимальная связность':
                intaktnost, iterations = AttackMin(graph)
            elif attack == 'Кластеризация':
                intaktnost, iterations = AttackClustering(graph)
            else:
                return

            if iterations != 0:
                goodGraphs += 1
            else:
                errors += 1

            intaktnostShare += intaktnost
            iterationsShare += iterations

        if intaktnostShare == 0:
            result = ('\nСредняя интактность для ' + str(self.j) + ' = ' + str(100) + '\n'
                      + 'Среднее количество удаленных вершин для ' + str(self.j) + ' = ' + str(self.size) + '\n'
                      + 'Средний успех для ' + str(self.j) + ' = ' + str(0) + '\n'
                      + 'Errors для ' + str(self.j) + ' = ' + str(errors/self.retry) + '\n')
            print(result)
        else:
            srIntaktnost = intaktnostShare / goodGraphs
            srIterations = float(iterationsShare / goodGraphs)
            srIterationsPercent = float(srIterations / self.size)
            srUspex = 1 - ((srIntaktnost * srIterations) / self.size)
            result = ('\nСредняя интактность для ' + str(self.j) + ' = ' + str(srIntaktnost*100) + '%\n'
                      + 'Среднее количество удаленных вершин для ' + str(self.j) + ' = ' + str(srIterationsPercent*100) + '%\n'
                      + 'Средний успех для ' + str(self.j) + ' = ' + str(srUspex*100) + '%\n'
                      + 'Errors для ' + str(self.j) + ' = ' + str(float(errors/self.retry)*100) + '%\n')
            print(result)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', default=100, type=int, required=False)
    parser.add_argument('-seed', default=None, type=int)
    parser.add_argument('-attack', choices=['Random', 'Centrality', 'Centrality with recalculation', 'Max', 'Min', 'Кластеризация'],
                        default='Кластеризация', required=False)
    parser.add_argument('-generate', choices=['Random', 'Ватца-Строгаца', 'Барабаши-Альберт'], default='Ватца-Строгаца', required=False)
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
    while j < size:
        j += 5
        if (j >= size):
            break
        thread = StartProgram(generate, attack, size, j, retry, seed)
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print(datetime.now() - start_time)
