import multiprocessing
from PyQt5.QtCore import QThread, pyqtSignal
import networkx as nx
import random
from matplotlib import pyplot as plt


def SaveGraph(graph, size, pos, path):
    if False:
        nx.draw(graph, node_size=size*100, with_labels=True, pos=pos, node_shape='o', font_size=size/5, font_color='red')
        plt.gcf().set_size_inches(size/5, size/5)
        fig = plt.savefig(path)
        plt.close(fig)
        print('SaveGraph')

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
                break

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


def GenerateIntaktnost(graph, size, pos):
    graphConnections = list(nx.connected_components(graph))
    intactness = 0

    for i in range(len(graphConnections)):
        nowGraph = nx.Graph()
        nowGraph.add_edges_from(graph.edges(graphConnections[i]))
        SaveGraph(nowGraph, size, pos, 'gif/finish%s.png' %i)

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
            intactness += currentGraphNodes*nowGraphNodes*2

    return 1 - intactness/(len(graph.nodes) ** 2)


def AttackClustering(graph):
    iteration = 0
    pos = nx.spring_layout(graph, k=0.3)
    clustering = nx.square_clustering(graph)
    clusteringList = list(clustering.items())
    clusteringList.sort(key=lambda i: i[1], reverse=True)
    size = len(graph.nodes)
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 10)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
        graph.remove_node(clusteringList[iteration][0])
        iteration += 1


def AttackRandom(graph):
    iteration = 0
    pos = nx.spring_layout(graph, k=0.3)
    size = len(graph.nodes)
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 10)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
        graph.remove_node(random.choice(list(graph.nodes())))
        iteration += 1


def AttackMax(graph):
    dic = {}
    for i in list(graph.edges):
        dic[i[0]] = 0
        dic[i[1]] = 0

    for i in list(graph.edges):
        dic[i[0]] = dic[i[0]] + 1
        dic[i[1]] = dic[i[1]] + 1

    maxList = list(dic.items())
    maxList.sort(key=lambda i: i[1], reverse=True)

    iteration = 0
    pos = nx.spring_layout(graph, k=0.3)
    size = len(graph.nodes)
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 10)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
        graph.remove_node(maxList[iteration][0])
        iteration += 1


def AttackMin(graph):
    dic = {}
    for i in list(graph.edges):
        dic[i[0]] = 0
        dic[i[1]] = 0

    for i in list(graph.edges):
        dic[i[0]] = dic[i[0]] + 1
        dic[i[1]] = dic[i[1]] + 1

    minList = list(dic.items())
    minList.sort(key=lambda i: i[1], reverse=True)
    node = minList.pop()

    iteration = 0
    pos = nx.spring_layout(graph, k=0.3)
    size = len(graph.nodes)
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 10)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)

        if (len(graph[node[0]]) != 0):
            pope = list(graph[node[0]]).pop()
            graph.remove_node(pope)

        iteration += 1


def AttackCentrality(graph):
    centrality = nx.eigenvector_centrality_numpy(graph)
    centralityList = list(centrality.items())
    centralitySorted = sorted(centralityList, key=lambda i: i[1])

    iteration = 0
    SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
    pos = nx.spring_layout(graph, k=0.3)
    size = len(graph.nodes)
    while True:
        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 5)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
        graph.remove_node(centralitySorted.pop()[0])
        iteration += 1


def AttackCentralityEach(graph):
    iteration = 0
    pos = nx.spring_layout(graph, k=0.3)
    size = len(graph.nodes)
    SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
    while True:

        if (len(graph.nodes) <= 1):
            return 0, 0

        if ((len(graph.nodes) == 0) and (len(graph.edges) != 0)):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if not nx.is_connected(graph):
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)
            intaktnost = GenerateIntaktnost(graph, size, pos)
            return intaktnost, iteration

        if ((iteration + 1) % (size / 20)) == 0:
            SaveGraph(graph, size, pos, 'gif/pic%s.png' % iteration)

        centrality = nx.eigenvector_centrality_numpy(graph, tol=1e-03)
        centralityList = list(centrality.items())
        centralitySorted = sorted(centralityList, key=lambda i: i[1])
        graph.remove_node(centralitySorted.pop()[0])
        iteration += 1


def RunCheckGraph(generate, attack, size, j, seed, iteration, return_dict):
    graph = nx.Graph()
    while 1:
        if generate == 'Случайный':
            graph = GenerateRandom(size, j, seed)
        elif generate == 'Ватц-Строгац':
            graph = GenerateSmallWorld(size, j, seed)
        elif generate == 'Барабаши-Альберт':
            graph = GenerateBarabasi(size, j, seed)
        else:
            return

        pos = nx.spring_layout(graph, k=0.3)
        SaveGraph(graph, size, pos, 'gif/pic0.png')
        if nx.is_connected(graph):
            break
        else:
            print('Graph is not connected, trying again')

    if attack == 'Случайная':
        intactness, iterations = AttackRandom(graph)
    elif attack == 'Центральность':
        intactness, iterations = AttackCentrality(graph)
    elif attack == 'Центральность с перерасчётом':
        intactness, iterations = AttackCentralityEach(graph)
    elif attack == 'Максимальная связность':
        intactness, iterations = AttackMax(graph)
    elif attack == 'Минимальная связность':
        intactness, iterations = AttackMin(graph)
    elif attack == 'Кластеризация':
        intactness, iterations = AttackClustering(graph)
    else:
        return

    error = 0
    if intactness == 0:
        error = 1

    if iterations == 0:
        global GraphNotConnected
        GraphNotConnected = True

    iterations = iterations/size
    return_dict[iteration] = [intactness, iterations, error]


class StartProgramThread(QThread):
    change_progress_bar = pyqtSignal(int)
    change_start_button = pyqtSignal(str)
    add_new_dialog = pyqtSignal(bool)
    intactness = pyqtSignal(float)
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
        global GraphNotConnected
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

        intactnessCommon = 0
        deletedNodes = 0
        errors = 0
        for ret in return_dict.values():
            intactnessCommon += ret[0]
            deletedNodes += ret[1]
            errors += ret[2]

        if (self.retry == errors):
            intactnessAvarage = 0
            deletedNodesAvarage = 0
        else:
            intactnessAvarage = intactnessCommon/(self.retry - errors) * 100
            deletedNodesAvarage = deletedNodes/(self.retry - errors) * 100

        self.intactness.emit(intactnessAvarage)
        self.deleted.emit(deletedNodesAvarage)
        self.errors.emit(errors/self.retry * 100)
        self.change_start_button.emit('Start')
        self.add_new_dialog.emit(True)
