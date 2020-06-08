import multiprocessing
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import networkx as nx
import random


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


def AttackRandom(graph):
    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            return 0, 0

        graph.remove_node(random.choice(list(graph.nodes())))

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
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
            return 0, 0

        graph.remove_node(list_d[iteration][0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
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
            return 0, 0

        if (len(graph[node[0]]) != 0):
            pope = list(graph[node[0]]).pop()
            graph.remove_node(pope)

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
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
            return 0, 0

        graph.remove_node(centralitySorted.pop()[0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def AttackCentralityEach(graph):
    iteration = 0
    while True:
        iteration += 1

        if (len(graph.nodes) <= 1):
            return 0, 0

        centrality = nx.eigenvector_centrality_numpy(graph, tol=1e-03)
        centralityList = list(centrality.items())
        centralitySorted = sorted(centralityList, key=lambda i: i[1])
        graph.remove_node(centralitySorted.pop()[0])

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            intaktnost = GenerateIntaktnost(graph)
            return intaktnost, iteration


def RunCheckGraph(generate, attack, size, j, seed, iteration, return_dict):
    if generate == 'Random':
        graph = GenerateRandom(size, j, seed)
    elif generate == 'Small world':
        graph = GenerateSmallWorld(size, j, seed)
    else:
        try:
            graph = GenerateBarabasi(size, j, seed)
        except:
            return_dict[iteration] = [1, size, 1]
            return

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
    return_dict[iteration] = [intaktnost, iterations, error]


class StartProgramThread(QThread):
    change_progress_bar = pyqtSignal(int)
    change_start_button = pyqtSignal(str)
    add_new_dialog = pyqtSignal(bool)
    intaktnost = pyqtSignal(float)
    deleted = pyqtSignal(float)
    errors = pyqtSignal(float)

    def __init__(self, retry: int, generate: str, attack: str, size: int, rewrite: int, seed):
        super().__init__()
        self.retry = retry
        self.generate = generate
        self.attack = attack
        self.size = size
        self.rewrite = rewrite
        self.seed = seed
        self.killThread = False

    def run(self):
        processes = []
        currRetry = 0
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        while (currRetry < self.retry) and not self.killThread:
            rangeProcess = []
            for j in range(12):
                p = multiprocessing.Process(target=RunCheckGraph, args=(self.generate, self.attack, self.size, self.rewrite, self.seed, currRetry, return_dict))
                processes.append(p)
                rangeProcess.append(p)
                p.start()

                if ((currRetry + 1) % (self.retry / 100)) == 0:
                    self.change_progress_bar.emit(int((currRetry + 1) / self.retry * 100))
                    #print(str((currRetry + 1) / self.retry * 100) + '%')

                currRetry += 1

                if (currRetry >= self.retry):
                    break;

                if (self.killThread):
                    return

            for process in rangeProcess:
                if (self.killThread):
                    return
                process.join()

        self.change_start_button.emit('Waiting')

        интактностьОбщая = 0
        удаленныеВершины = 0
        ошибки = 0
        for ret in return_dict.values():
            интактностьОбщая += ret[0]
            удаленныеВершины += ret[1]
            ошибки += ret[2]

        print('Интактность общая: ' + str(интактностьОбщая/(self.retry - ошибки) * 100) + '%')
        self.intaktnost.emit(интактностьОбщая/(self.retry - ошибки) * 100)
        print('Удаленные вершины: ' + str(удаленныеВершины/(self.retry - ошибки) * 100) + '%')
        self.deleted.emit(удаленныеВершины/(self.retry - ошибки) * 100)
        print('Ошибки: ' + str(ошибки/self.retry * 100) + '%')
        self.errors.emit(ошибки/self.retry * 100)
        self.change_start_button.emit('Start')
        self.add_new_dialog.emit(True)
