import networkx as nx
import json


def generate_simple_graph() -> nx.Graph:
    """
        Function generates small weighted graph.
    """

    # node_list = [(0, dict(position=[15, 20])),
    #              (1, dict(position=[10, 15])),
    #              (2, dict(position=[20, 15])),
    #              (3, dict(position=[5, 10])),
    #              (4, dict(position=[15, 10])),
    #              (5, dict(position=[25, 10])),
    #              (6, dict(position=[0, 5])),
    #              (7, dict(position=[10, 5])),
    #              (8, dict(position=[20, 5])),
    #              (9, dict(position=[30, 5])),
    #              (10, dict(position=[0, 0])),
    #              (11, dict(position=[10, 0])),
    #              (12, dict(position=[20, 0])),
    #              (13, dict(position=[30, 0])),
    #             ]
    #
    # edge_list = [(0, 1, 3),
    #              (0, 2, 1),
    #              (1, 3, 5),
    #              (2, 4, 1),
    #              (2, 5, 4),
    #              (3, 6, 7),
    #              (4, 7, 1),
    #              (4, 8, 8),
    #              (5, 9, 2),
    #              (6, 10, 9),
    #              (8, 12, 8),
    #              (9, 13, 4),
    #              (10, 11, 1),
    #              (11, 12, 8),
    #              (7, 11, 1)]
    #
    #
    # json_object = json.dumps({"node_list": node_list,
    #                           "edge_list": edge_list}, indent=4)
    # with open("simple graph.json", "w") as outfile:
    #     outfile.write(json_object)

    with open('utils/graphs/simple graph.json', 'r') as openfile:
        graph_info = json.load(openfile)

    graph = nx.Graph()
    graph.add_nodes_from(graph_info["node_list"])
    graph.add_weighted_edges_from(graph_info["edge_list"])
    start_node = 0
    goal_node = 10
    return graph, start_node, goal_node


def generate_maze_graph():
    def str_to_int(lst):
        return list(map(int, lst))

    input_file = open("utils/graphs/maze.txt", "r")
    input_from_file = input_file.readlines()
    maze_list = [str_to_int(x.rstrip().split()) for x in input_from_file]

    node_list, edge_list = [], []
    nodenum_by_pos = dict()
    node_num = 0

    for i in range(len(maze_list)):
        for j in range(len(maze_list[0])):
            if maze_list[i][j] == 1:
                continue
            node_list.append((node_num, dict(position=[j, len(maze_list) - i])))
            nodenum_by_pos[(i, j)] = node_num
            # vertical edge
            if i > 0 and maze_list[i - 1][j] == 0:
                edge_list.append((node_num, nodenum_by_pos[(i - 1, j)], 1))

            # horizontal edge
            if j > 0 and maze_list[i][j - 1] == 0:
                edge_list.append((node_num, node_num - 1, 1))

            node_num += 1

    maze = nx.Graph()
    maze.add_nodes_from(node_list)
    maze.add_weighted_edges_from(edge_list)

    return maze, 113, 198, maze_list


def print_path(goal_node, parent):

    current_node = goal_node
    path_string = str(goal_node)
    while current_node in parent:
        current_node = parent[current_node]
        path_string = str(current_node) + ' -> ' + path_string
    print(path_string)
    return 0