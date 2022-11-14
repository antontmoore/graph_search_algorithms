import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_structures import Stack
from data_structures import Queue
from data_structures import DijkstraQueue
from data_structures import AStarQueue
import plotly.io as pio
import networkx as nx

THEMECOLORS = {
    'background': '#1e1e1e',
    'dark-grey': '#252526',
    'medium-grey': '#2d2d2d',
    'light-grey': '#3c3c3c',
    'blue': '#0079cc',
    'dark-blue': '#0065bb',
    'light-blue': '#569cd6',
    'magenta': '#69217a',
    'light-magenta': '#da71d6',
    'green': '#24c93e',
    'white': '#d0d0d0',
    'black': '#101010',
}

class GraphAnimator():
    def __init__(self, graph, start_node, target_node, is_maze=False, maze_list=[], edge_weight=False):
        self.graph = graph
        self.start_node = start_node
        self.target_node = target_node
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
                      color=THEMECOLORS["light-grey"]),
            hoverinfo='none',
            mode='lines',
            showlegend=False,
            text="5")

        return edge_trace


    def get_node_trace(self, color):
        node_x = []
        node_y = []
        for node in self.graph.nodes():
            x, y = self.graph.nodes[node]['position']
            node_x.append(x)
            node_y.append(y)

        node_colors, node_text_colors = [None for _ in color], [None for _ in color]
        for idx, c in enumerate(color):
            if idx == self.start_node:
                node_colors[idx] = THEMECOLORS['light-blue']
                node_text_colors[idx] = THEMECOLORS['dark-grey']
            elif idx == self.target_node:
                node_colors[idx] = THEMECOLORS['green']
                node_text_colors[idx] = THEMECOLORS['dark-grey']
            elif c == 'white':
                node_colors[idx] = THEMECOLORS['white']
                node_text_colors[idx] = THEMECOLORS['black']
            elif c == 'grey':
                node_colors[idx] = THEMECOLORS['light-grey']
                node_text_colors[idx] = THEMECOLORS['blue']
            elif c == 'black':
                node_colors[idx] = THEMECOLORS['black']
                node_text_colors[idx] = THEMECOLORS['blue']


        node_text = list(self.graph.nodes())
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                reversescale=True,
                color=node_colors,
                size=18 if self.is_maze else 35,
                line_width=1 if self.is_maze else 2,
                line=dict(color=THEMECOLORS['medium-grey'], width=0.5)),
            showlegend=False,
            textposition="middle center",
            text=[] if self.is_maze else node_text,
            textfont=dict(family="arial",
                          size=10 if self.is_maze else 18,
                          color=node_text_colors))

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
            line=dict(width=3, color=THEMECOLORS['green']),  #'#33FF33'
            hoverinfo='none',
            mode='lines',
            showlegend=False)

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

    def get_contour_trace(self, nodes_storage):

        if isinstance(nodes_storage, Stack):
            contour_x = [-1, -1, 1, 1]
            contour_y = [4.5, -0.5, -0.5, 4.5]
        else:
            contour_x = [-1.2, -1, -1, -0.9, None, 0.8, 1, 1, 1.2]
            contour_y = [4.7, 4.5, -0.5, -0.7, None, -0.7, -0.5, 4.5, 4.7]

        contour_trace = go.Scatter(
            x=contour_x, y=contour_y,
            line=dict(width=3,
                      color=THEMECOLORS['dark-blue']),
            hoverinfo='none',
            mode='lines',
            showlegend=False,
            xaxis="x2", yaxis="y2")

        return contour_trace

    def get_nodes_storage_trace(self, nodes_storage):

        y_coord = list(range(len(nodes_storage.nodes)))
        x_coord = [0] * len(nodes_storage.nodes)
        nodes = nodes_storage.nodes
        node_colors = [THEMECOLORS['light-grey']] * len(nodes)
        node_text_colors = [THEMECOLORS['blue']] * len(nodes)
        for idx, node_id in enumerate(nodes):
            if node_id == self.start_node:
                node_colors[idx] = THEMECOLORS['light-blue']
                node_text_colors[idx] = THEMECOLORS['dark-grey']
            elif node_id == self.target_node:
                node_colors[idx] = THEMECOLORS['green']
                node_text_colors[idx] = THEMECOLORS['dark-grey']

        node_storage_trace = go.Scatter(
            x=x_coord, y=y_coord,
            xaxis="x2", yaxis="y2",
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=18 if self.is_maze else 35,
                line_width=1 if self.is_maze else 2,
                line=dict(color=THEMECOLORS['light-grey'], width=0.5)),
            textposition="middle center",
            showlegend=False,
            text=nodes_storage.nodes,
            textfont=dict(family="arial",
                          size=10 if self.is_maze else 16,
                          color=node_text_colors))

        return node_storage_trace


    def add_frame(self, color, came_from, current_node, nodes_storage):
        edge_trace = self.get_edge_trace()
        node_trace = self.get_node_trace(color)
        path_trace = self.get_path_trace(came_from, current_node)
        contour_trace = self.get_contour_trace(nodes_storage)
        nodes_storage_trace = self.get_nodes_storage_trace(nodes_storage)

        new_frame = [edge_trace, path_trace, node_trace, contour_trace, nodes_storage_trace]
        self.frames.append(new_frame)
        return 0

    def make_frame_with_storage(self, color, came_from, current_node, nodes_storage):
        edge_trace = self.get_edge_trace()
        node_trace = self.get_node_trace(color)
        path_trace = self.get_path_trace(came_from, current_node)

        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.8, 0.2],
            )

        fig.add_trace(edge_trace, row=1, col=1)
        fig.add_trace(node_trace, row=1, col=1)
        fig.add_trace(path_trace, row=1, col=1)

        y_coord = list(range(len(nodes_storage.nodes)))
        x_coord = [0] * len(nodes_storage.nodes)

        node_storage_trace = go.Scatter(
            x=x_coord, y=y_coord,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=[THEMECOLORS['light-grey'] for _ in nodes_storage.nodes],
                size=35,
                line_width=2,
                line=dict(color="white", width=0.5)),
            textposition="middle center",
            showlegend=False,
            text=nodes_storage.nodes,
            textfont=dict(family="arial",
                          size=10 if self.is_maze else 16,
                          color='#4e4eAe'))
        fig.add_trace(
            node_storage_trace,
            row=1, col=2,
        ).update_layout(yaxis2=dict(range=[-2, 6]), xaxis2=dict(range=[-2, 2]))

        # контур хранилища
        nodes_storage_name = str(type(nodes_storage)).split('.')[1].split('\'')[0]
        if isinstance(nodes_storage, Stack):
            contour_x = [-1, -1, 1, 1]
            contour_y = [4.5, -0.5, -0.5, 4.5]
        else:
            contour_x = [-0.8, -1, -1, -1.2, None, 1.2, 1, 1, 0.8]
            contour_y = [4.7, 4.5, -0.5, -0.7, None, -0.7, -0.5, 4.5, 4.7]

        contour_trace = go.Scatter(
            x=contour_x, y=contour_y,
            line=dict(width=3,
                      color='#aaaaaa'),
            hoverinfo='none',
            mode='lines',
            showlegend=False)
        fig.add_trace(
            contour_trace,
            row=1, col=2)

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.add_annotation(x=-1.5, xref="x2",
                           y=2, yref="y2",
                           text=nodes_storage_name, textangle=-90,
                           align="center",
                           showarrow=False,
                           font=dict(size=25, color="#000000")
                           )
        if isinstance(nodes_storage, Stack):
            fig.add_annotation(x=-0.5, y=4.5, ax=-0.5, ay=5., text="",
                               xref='x2', yref='y2', axref='x2', ayref='y2',
                               showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=2, arrowcolor='black')
            fig.add_annotation(x=0.5, y=5., ax=0.5, ay=4.5, text="",
                               xref='x2', yref='y2', axref='x2', ayref='y2',
                               showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=2, arrowcolor='black')
        else:
            fig.add_annotation(x=0., y=-1., ax=0., ay=-1.5, text="",
                               xref='x2', yref='y2', axref='x2', ayref='y2',
                               showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=2, arrowcolor='black')
            fig.add_annotation(x=0., y=5.5, ax=0., ay=5., text="",
                               xref='x2', yref='y2', axref='x2', ayref='y2',
                               showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=2, arrowcolor='black')

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Step:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }
        steps = list(range(8))
        for step in range(8):
            slider_step = {"args": [
                [step],
                {"frame": {"duration": 300, "redraw": False},
                 "mode": "immediate",
                 "transition": {"duration": 300}}
            ],
                "label": step,
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)


        fig.layout.sliders = [sliders_dict]
        fig.show()

        return 0

    def make_data_from_traces(self, frame_num):
        edge_trace = self.frames[frame_num][0]
        edge_node = {"x": list(edge_trace.x),
                     "y": list(edge_trace.y),
                     "mode": edge_trace.mode,
                     "hoverinfo": edge_trace.hoverinfo,
                     "line": edge_trace.line,
                     "showlegend": edge_trace.showlegend,
                     }

        path_trace = self.frames[frame_num][1]
        data_path = {"x": list(path_trace.x),
                     "y": list(path_trace.y),
                     "line": path_trace.line,
                     "hoverinfo": path_trace.hoverinfo,
                     "mode": path_trace.mode,
                     "showlegend": path_trace.showlegend
                     }

        node_trace = self.frames[frame_num][2]
        data_node = {"x": list(node_trace.x),
                     "y": list(node_trace.y),
                     "text": list(node_trace.text),
                     "mode": node_trace.mode,
                     "hoverinfo": node_trace.hoverinfo,
                     "marker": node_trace.marker,
                     "showlegend": node_trace.showlegend,
                     "textfont": node_trace.textfont,
                     }

        contour_trace = self.frames[frame_num][3]
        data_contour = {"x": list(contour_trace.x),
                        "y": list(contour_trace.y),
                        "xaxis": contour_trace.xaxis,
                        "yaxis": contour_trace.yaxis,
                        "line": contour_trace.line,
                        "hoverinfo": contour_trace.hoverinfo,
                        "mode": contour_trace.mode,
                        "showlegend": contour_trace.showlegend,
                        }

        nodes_storage_trace = self.frames[frame_num][4]
        data_nodes_storage = {"x": list(nodes_storage_trace.x),
                              "y": list(nodes_storage_trace.y),
                              "xaxis": nodes_storage_trace.xaxis,
                              "yaxis": nodes_storage_trace.yaxis,
                              "mode": nodes_storage_trace.mode,
                              "hoverinfo": nodes_storage_trace.hoverinfo,
                              "marker": nodes_storage_trace.marker,
                              "textposition": nodes_storage_trace.textposition,
                              "showlegend": nodes_storage_trace.showlegend,
                              "text": nodes_storage_trace.text,
                              "textfont": nodes_storage_trace.textfont,
                              }

        return [edge_node, data_path, data_node, data_contour, data_nodes_storage]

    def make_animation_with_storage(self, color, came_from, current_node, nodes_storage):

        # Create initially empty dictionary
        fig_dict = {
            "data": [],
            "layout": {},
            "frames": []
        }

        fig_dict["layout"]["xaxis"] = {"showgrid": False, "zeroline": False, "showticklabels": False,
                                       "anchor": 'y', "domain": [0.0, 0.75]}
        fig_dict["layout"]["yaxis"] = {"showgrid": False, "zeroline": False, "showticklabels": False,
                                       "anchor": 'x', "domain": [0.0, 1.0]}
        fig_dict["layout"]["xaxis2"] = {"showgrid": False, "zeroline": False, "showticklabels": False,
                                        "anchor": 'y2', "domain": [0.80, 1.0], "range": (-2., 2.)}
        fig_dict["layout"]["yaxis2"] = {"showgrid": False, "zeroline": False, "showticklabels": False,
                                        "anchor": 'x2', "domain": [0.0, 1.0], "range": (-2., 6.)}
        fig_dict["layout"]["margin"] = dict(l=0, r=0, b=0, t=0)

        fig_dict["layout"]["plot_bgcolor"] = THEMECOLORS['background']
        fig_dict["layout"]["paper_bgcolor"] = THEMECOLORS['background']
        fig_dict["layout"]["font_color"] = THEMECOLORS['blue']

        # annotations
        nodes_storage_name = str(type(nodes_storage)).split('.')[1].split('\'')[0]
        storage_name = {"align": 'center',
                        "font": {"color": THEMECOLORS['dark-blue'], "size": 25},
                        "text": nodes_storage_name,
                        "textangle": -90,
                        "x": -1.5, "y": 2.0,
                        "ax": 0., "ay": 0.,
                        "xref": "x2", "yref": "y2"
                        }
        x_arrow, y_arrow, ax_arrow, ay_arrow = \
            (-0.5, 4.5, -0.5, 5.3) if isinstance(nodes_storage, Stack) else (0.0, 5.0, 0.0, 5.8)
        arrow_in = {"arrowcolor": THEMECOLORS['dark-blue'],
                    "arrowhead": 2, "arrowsize": 1, "arrowwidth": 2,
                    "ax": ax_arrow, "ay": ay_arrow,
                    "x": x_arrow, "y": y_arrow,
                    "axref": "x2", "ayref": "y2",
                    "xref": "x2", "yref": "y2",
                    "showarrow": True,
                    }

        x_arrow, y_arrow, ax_arrow, ay_arrow = \
            (0.5, 5.3, 0.5, 4.5) if isinstance(nodes_storage, Stack) else (0.0, -1.8, 0.0, -1.0)
        arrow_out = {"arrowcolor": THEMECOLORS['dark-blue'],
                     "arrowhead": 2, "arrowsize": 1, "arrowwidth": 2,
                     "ax": ax_arrow, "ay": ay_arrow,
                     "x": x_arrow, "y": y_arrow,
                     "axref": "x2", "ayref": "y2",
                     "xref": "x2", "yref": "y2",
                     "showarrow": True,
                     }

        start_node_text_coordinates = (-2., 9.) if self.is_maze else (17., 20.5)
        target_node_text_coordinates = (22., 4.) if self.is_maze else (2., -1.)
        start_node_text = {"align": 'left',
                           "font": {"color": THEMECOLORS['light-blue'], "size": 25},
                           "text": "start",
                           "x": start_node_text_coordinates[0],
                           "y": start_node_text_coordinates[1],
                           "xref": "x", "yref": "y",
                           "showarrow": False
                           }
        target_node_text = {"align": 'left',
                          "font": {"color": THEMECOLORS['green'], "size": 25},
                          "text": "target",
                          "x": target_node_text_coordinates[0],
                          "y": target_node_text_coordinates[1],
                          "xref": "x", "yref": "y",
                          "showarrow": False
                          }

        fig_dict["layout"]["annotations"] = [storage_name, arrow_in, arrow_out, start_node_text, target_node_text]

        # edge annotations
        if not self.is_maze:
            edges = list(self.graph.edges)
            weight_by_edge = nx.get_edge_attributes(self.graph, 'weight')
            edge_annotations = []
            for edge in edges:
                x_start, y_start = self.graph.nodes[edge[0]]['position']
                x_end, y_end = self.graph.nodes[edge[1]]['position']

                if y_start == y_end:
                    x_text = (x_start + x_end) / 2
                    y_text = (y_start + y_end) / 2 + 0.5
                elif x_start == x_end:
                    x_text = (x_start + x_end) / 2 + 0.5
                    y_text = (y_start + y_end) / 2
                elif (x_end - x_start) * (y_end - y_start) > 0:
                    x_text = (x_start + x_end) / 2 - 0.5
                    y_text = (y_start + y_end) / 2 + 0.5
                else:
                    x_text = (x_start + x_end) / 2 + 0.5
                    y_text = (y_start + y_end) / 2 + 0.5

                edge_weight_text = {"align": 'left',
                                    "font": {"color": THEMECOLORS['light-grey'], "size": 15},
                                    "text": str(weight_by_edge[edge]),
                                    "x": x_text,
                                    "y": y_text,
                                    "xref": "x", "yref": "y",
                                    "showarrow": False
                                    }
                edge_annotations.append(edge_weight_text)

            fig_dict["layout"]["annotations"].extend(edge_annotations)


        # make data
        fig_dict["data"] = self.make_data_from_traces(0)

        sliders_dict = {
            "active": 0,
            "activebgcolor": THEMECOLORS['light-blue'],
            "bordercolor": THEMECOLORS['medium-grey'],
            "bgcolor": THEMECOLORS['blue'],
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Step:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        # make frames
        for frame_num in range(len(self.frames)):
            frame = {"data": self.make_data_from_traces(frame_num),
                     "name": str(frame_num)}


            fig_dict["frames"].append(frame)

            slider_step = {"args": [
                [frame_num],
                {"frame": {"duration": 300, "redraw": False},
                 "mode": "immediate",
                 "transition": {"duration": 300}}
            ],
                "label": frame_num,
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": False},
                                        "fromcurrent": True, "transition": {"duration": 300,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                          "mode": "immediate",
                                          "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
                "bordercolor": THEMECOLORS['blue'],
                "bgcolor": THEMECOLORS['dark-grey'],
            }
        ]

        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)
        fig.show()

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
                           text="target", showarrow=False,
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
                           text="target", showarrow=False,
                           font=dict(family="arial", size=25, color="#FF8888")
                           )

        return fig