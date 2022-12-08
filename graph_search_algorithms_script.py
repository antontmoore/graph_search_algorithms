from utils import generate_simple_graph, generate_maze_graph, print_path
from data_structures import *
from utils import GraphAnimator
from networkx import Graph


def find_path(
        graph: Graph,
        start_node: int,
        target_node: int,
        nodes_storage_structure_name: str,
        animator: GraphAnimator
    ):
    """
        Universal algorithm for traversing graph searching the path from start_node to target_node.
        It uses graph structure and the auxilary node storage structure.
        The animator is used to create animations of the search process.
    """

    color = ['white'] * graph.number_of_nodes()      # coloring all nodes to white
    dist = [float('Inf')] * graph.number_of_nodes()  # the distances to all the nodes at the start are infinity
    parent = dict()                                  # dictionary {node : its parent}

    nodes_storage = {
        'Stack': Stack(),
        'Queue': Queue(),
        'DijkstraQueue': DijkstraQueue(dist),
        'AStarQueue': AStarQueue(graph, dist, target_node)
    }[nodes_storage_structure_name]

    # place the start node to the storage
    nodes_storage.insert(start_node)
    dist[start_node] = 0
    animator.add_frame(color, parent, start_node, nodes_storage)

    # Loop until there are nodes in storage
    while not nodes_storage.is_empty():
        current_node = nodes_storage.get_first()

        if current_node == target_node:
            # End of the search, the target is found.
            print_path(target_node, parent)
            animator.add_frame(color, parent, current_node, nodes_storage)
            break

        # take all the neighbours of the current node
        neighbours = list(graph.adj[current_node])
        for node_to_go in neighbours:
            if color[node_to_go] == 'white':            # if this neighbour is new to us
                color[node_to_go] = 'grey'              # paint in grey
                parent[node_to_go] = current_node       # saving the parent (where we came from)
                dist[node_to_go] = dist[current_node] + graph.get_edge_data(node_to_go, current_node)['weight']
                nodes_storage.insert(node_to_go)  # add to node storage
            else:
                # Otherwise we have to solve the conflict of duplicates
                # comparing the distance from the current node to the neighbor
                # with the distance to it along the previously found path
                weight_from_current_node = graph.get_edge_data(node_to_go, current_node)['weight']
                if dist[current_node] + weight_from_current_node < dist[node_to_go]:
                    dist[node_to_go] = dist[current_node] + weight_from_current_node

        # painting the current node in black, we won't come back here
        color[current_node] = 'black'
        animator.add_frame(color, parent, current_node, nodes_storage)
        # animator.make_frame_with_storage(color, parent, current_node, nodes_storage)

    # fig = graph_animator.make_animation()
    animator.make_animation_with_storage(color, parent, target_node, nodes_storage)
    # fig.show()


# Building small simple graph
graph, start_node, target_node = generate_simple_graph()

# Create helper class for pretty animations and make a first shot
graph_animator = GraphAnimator(graph, start_node, target_node, show_controls=True)

# DFS on simple graph
find_path(graph, start_node, target_node, 'Stack', graph_animator)

# BFS on simple graph
# find_path(graph, start_node, target_node, 'Queue', graph_animator)

# Dijkstra algorithm on simple graph
# graph_animator = GraphAnimator(graph, start_node, target_node,
#                                show_edge_weight=True, show_controls=True)
# find_path(graph, start_node, target_node, 'DijkstraQueue', graph_animator)

# graph, start_node, target_node, maze_list = generate_maze_graph()
# graph_animator = GraphAnimator(graph, start_node, target_node,
#                                is_maze=True, maze_list=maze_list,
#                                show_datastructure=False)

# Dijkstra algorithm on large graph
# find_path(graph, start_node, target_node, 'DijkstraQueue', graph_animator)

# A* algorithm on large graph
find_path(graph, start_node, target_node, 'AStarQueue', graph_animator)
