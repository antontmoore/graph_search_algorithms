from abc import ABC
from abc import abstractmethod
from math import sqrt
from heapq import heappush
from heapq import heappop


class AbstractNodeStorageClass(ABC):
    """
        Abstract class for all the data structures.
        All of them must have methods:
         - insert - to add element inside data structure;
         - get_first - to extract the most appropriate element from the data structure;
         - empty - return the boolean flag, if the structure still have any element inside.
    """

    @abstractmethod
    def get_first(self):
        pass

    @abstractmethod
    def insert(self, element):
        pass

    @abstractmethod
    def is_empty(self):
        pass


class Stack(AbstractNodeStorageClass):
    """
        Simple stack works on a LIFO (Last In, First Out) principle
    """
    def __init__(self):
        self.nodes = []

    def get_first(self):
        return self.nodes.pop()

    def insert(self, node_number):
        self.nodes.append(node_number)

    def is_empty(self):
        return len(self.nodes) == 0


class Queue(AbstractNodeStorageClass):
    """
        Simple queue works on a FIFO (First In, First Out) principle
    """

    def __init__(self):
        self.nodes = []

    def get_first(self):
        return self.nodes.pop(0)

    def insert(self, node_number):
        self.nodes.append(node_number)

    def is_empty(self):
        return len(self.nodes) == 0


class DijkstraQueue(AbstractNodeStorageClass):
    """
        Priority queue for Dijkstra's method.
        In the get_first() method, it selects a node,
        with a minimal distance from the start node,
        using heap datastructure.
    """

    def __init__(self, distances):
        self.nodes = []
        self.distances = distances

    def get_first(self):
        closest_node_distance, closest_node = heappop(self.nodes)
        return closest_node

    def insert(self, element):
        heappush(self.nodes, (self.distances[element], element))

    def is_empty(self):
        return len(self.nodes) == 0


class AStarQueue(AbstractNodeStorageClass):
    """
        Priority queue for AStar method.
        In the get_first() method, a node is selected that has the minimum distance to the start node
        and the minimum estimate (according to heuristics) to the end node.
    """

    def __init__(self, graph, distances, goal_node):
        self.nodes = []
        self.graph = graph
        self.x_goal, self.y_goal = graph.nodes[goal_node]['position']
        self.distances = distances

    def calc_heuristic(self, node):
        x_node, y_node = self.graph.nodes[node]['position']
        estimated_distance_to_goal = sqrt(
            (x_node - self.x_goal) ** 2 +
            (y_node - self.y_goal) ** 2
        )
        return estimated_distance_to_goal

    def get_first(self):
        optimal_node_value, optimal_node = heappop(self.nodes)
        return optimal_node

    def insert(self, element):
        heappush(self.nodes,
                 (self.distances[element] +
                  self.calc_heuristic(element), element)
                 )

    def is_empty(self):
        return len(self.nodes) == 0
