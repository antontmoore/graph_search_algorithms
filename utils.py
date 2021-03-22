import networkx as nx


def generate_graph():

    graph = nx.Graph()
    node_list = [(0, dict(pos=[15, 20])),
                 (1, dict(pos=[10, 15])),
                 (2, dict(pos=[20, 15])),
                 (3, dict(pos=[5, 10])),
                 (4, dict(pos=[15, 10])),
                 (5, dict(pos=[25, 10])),
                 (6, dict(pos=[0, 5])),
                 (7, dict(pos=[10, 5])),
                 (8, dict(pos=[20, 5])),
                 (9, dict(pos=[30, 5])),
                 (10, dict(pos=[0, 0])),
                 (11, dict(pos=[10, 0])),
                 (12, dict(pos=[20, 0])),
                 (13, dict(pos=[30, 0])),
                ]


    graph.add_nodes_from(node_list)
    edge_list = [(0, 1, 3), (0, 2, 1), (1, 3, 5), (2, 4, 1), (2, 5, 4), (3, 6, 7), (4, 7, 1), (4, 8, 8), (5, 9, 2), (6, 10, 9), (8, 12, 8), (9, 13, 4),
                 (10, 11, 1), (11, 12, 8), (7, 11, 1)]
    graph.add_weighted_edges_from(edge_list)
    return graph


def generate_maze():
    def str_to_int(lst):
        return list(map(int, lst))

    input_file = open("maze1.txt", "r")
    input_from_file = input_file.readlines()
    maze_list = [str_to_int(x.rstrip().split()) for x in input_from_file]

    node_list, edge_list = [], []
    nodenum_by_pos = dict()
    node_num = 0
    rowlen = len(maze_list[0])
    for i in range(len(maze_list)):
        for j in range(rowlen):
            if maze_list[i][j] == 1:
                continue
            node_list.append((node_num, dict(pos=[j, len(maze_list)-i])))
            nodenum_by_pos[(i, j)] = node_num
            # вверх
            if i > 0 and maze_list[i-1][j] == 0:
                edge_list.append((node_num, nodenum_by_pos[(i-1, j)], 1))

            # # вниз
            # if i < len(maze_list)-1 and maze_list[i+1][j] == 0:
            #     edge_list.append((node_num, node_num + rowlen, 1))

            # влево
            if j > 0 and maze_list[i][j-1] == 0:
                edge_list.append((node_num, node_num-1, 1))

            # # вправо
            # if j < rowlen-1 and maze_list[i][j+1] == 0:
            #     edge_list.append((node_num, node_num+1, 1))

            node_num += 1

    maze = nx.Graph()
    maze.add_nodes_from(node_list)
    maze.add_weighted_edges_from(edge_list)
    print('start_node = ', nodenum_by_pos[(8, 0)], '; goal_node = ', nodenum_by_pos[(13, 20)])
    return maze, maze_list


def print_path(goal_node, parent):
  current_node = goal_node
  path_string = str(goal_node)
  while current_node in parent:
    current_node = parent[current_node]
    path_string = str(current_node) + ' -> ' + path_string
  print(path_string)
  return 0