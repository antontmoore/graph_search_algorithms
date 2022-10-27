import plotly.graph_objects as go


class GraphAnimator():
    def __init__(self, graph, start_node, goal_node, is_maze=False, maze_list=[], edge_weight=False):
        self.graph = graph
        self.start_node = start_node
        self.goal_node = goal_node
        self.frames = []
        self.start_frame = None
        self.is_maze = is_maze
        self.maze_list = maze_list
        self.edge_weight = edge_weight
        self.edge_list = [
            (0, 1, 3),
            (0, 2, 1),
            (1, 3, 5),
            (2, 4, 1), (2, 5, 4), (3, 6, 7), (4, 7, 1), (4, 8, 8), (5, 9, 2), (6, 10, 9), (8, 12, 8), (9, 13, 4),
                 (10, 11, 1), (11, 12, 8), (7, 11, 1)]


    def get_edge_trace(self):
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = self.graph.nodes[edge[0]]['position']
            x1, y1 = self.graph.nodes[edge[1]]['position']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1 if self.is_maze else 3,
                      color='#aaaaaa'),
            hoverinfo='none',
            mode='lines')

        return edge_trace


    def get_node_trace(self, color):
        node_x = []
        node_y = []
        for node in self.graph.nodes():
            x, y = self.graph.nodes[node]['position']
            node_x.append(x)
            node_y.append(y)

        node_colors = [c for c in color]
        node_colors[self.start_node] = "LightSeaGreen"
        node_colors[self.goal_node] = "#FF8888"
        node_text = list(self.graph.nodes())
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Greens',
                reversescale=True,
                color=node_colors,
                size=18 if self.is_maze else 35,
                line_width=1 if self.is_maze else 2,
                line=dict(color="white", width=0.5)),
            textposition="middle center",
            text=[] if self.is_maze else node_text,
            textfont=dict(family="arial",
                          size=10 if self.is_maze else 16,
                          color='#4e4eAe'))

        return node_trace


    def get_path_trace(self, came_from, current_node):
        node_to = current_node
        edge_x, edge_y = [], []
        while node_to is not self.start_node:
            node_from = came_from[node_to]
            x0, y0 = self.graph.nodes[node_from]['position']
            x1, y1 = self.graph.nodes[node_to]['position']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
            node_to = node_from

        path_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=3, color='#33FF33'),
            hoverinfo='none',
            mode='lines')

        return path_trace

    def get_maze_trace(self):
        xm, ym = [], []
        rows = len(self.maze_list)
        for i in range(len(self.maze_list)):
            for j in range(len(self.maze_list[0])):
                if self.maze_list[i][j] == 1:
                    ym.extend([rows - (i-0.5), rows - (i-0.5), rows - (i+0.5), rows - (i+0.5), None])
                    xm.extend([j-0.5, j+0.5, j+0.5, j-0.5, None])
        maze_trace = go.Scatter(x=xm, y=ym, fill="toself")
        return maze_trace

    def add_frame(self, color, came_from, current_node):
        edge_trace = self.get_edge_trace()
        node_trace = self.get_node_trace(color)
        path_trace = self.get_path_trace(came_from, current_node)

        new_frame = [edge_trace, path_trace, node_trace]
        self.frames.append(new_frame)
        return 0

    def make_animation(self):
        maze_trace = self.get_maze_trace()
        fig = go.Figure(
            data=[self.frames[0][0], self.frames[0][1], self.frames[0][2], maze_trace],
            layout=go.Layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='#1e1e55',
                showlegend=False,
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None])])]
            ),
            frames=[go.Frame(data=[self.frames[k][0], self.frames[k][1], self.frames[k][2]])
                    for k in range(len(self.frames))]
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.add_annotation(x=-2 if self.is_maze else 13,
                           y=9 if self.is_maze else 20,
                           text="start", showarrow=False,
                           font=dict(family="arial", size=25, color="LightSeaGreen")
                           )
        fig.add_annotation(x=22 if self.is_maze else -2,
                           y=4 if self.is_maze else 0,
                           text="goal", showarrow=False,
                           font=dict(family="arial", size=25, color="#FF8888")
                           )
        if self.edge_weight:
            for edge in self.edge_list:
                x0, y0 = self.graph.nodes[edge[0]]['pos']
                x1, y1 = self.graph.nodes[edge[1]]['pos']
                w = edge[2]
                fig.add_annotation(x=(x0+x1)/2+1,
                                   y=(y0+y1)/2,
                                   text=str(w), showarrow=False,
                                   font=dict(family="arial", size=25, color="#DD0000")
                                   )

        return fig

    def make_one_shot(self):
        edge_trace = self.get_edge_trace()
        node_trace = self.get_node_trace(['white' for _ in range(self.graph.number_of_nodes())])
        maze_trace = self.get_maze_trace()
        fig = go.Figure(
            data=[edge_trace, node_trace, maze_trace],
            layout=go.Layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='#1e1e55',
                showlegend=False,
            )
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.add_annotation(x=-2 if self.is_maze else 13,
                           y=9 if self.is_maze else 20,
                           text="start", showarrow=False,
                           font=dict(family="arial", size=25, color="LightSeaGreen")
                           )
        fig.add_annotation(x=22 if self.is_maze else -2,
                           y=4 if self.is_maze else 0,
                           text="goal", showarrow=False,
                           font=dict(family="arial", size=25, color="#FF8888")
                           )

        return fig