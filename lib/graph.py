from typing import Tuple, List, Any
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import json
import os


class Vertex:
    def __init__(self, data: Any, in_degree: int = 0, out_degree: int = 0) -> None:
        """This constructor initialized the vertex object

        param
            data: any type of data associated with the vertex
            in_degree: the in degree count of the vertex
            out_degree: the out degree count of the vertex

        :return: None
        """
        self.data = data
        self.in_degree = in_degree
        self.out_degree = out_degree

    def increment_in_degree(self) -> None:
        """This function increments the counter in degree

        :return: None
        """
        self.in_degree += 1

    def decrement_in_degree(self) -> None:
        """This function decrements the counter in degree

        :return: None
        """
        self.in_degree -= 1

    def increment_out_degree(self) -> None:
        """This function increments the counter out degree

        :return: None
        """
        self.out_degree += 1

    def decrement_out_degree(self) -> None:
        """This function decrements the counter out degree

        :return: None
        """
        self.out_degree -= 1

    def get_state(self) -> Tuple[Any, int, int]:
        """This functions gets the state of the vertex

        :return: data, in degree count, out degree count
        """
        return self.data, self.in_degree, self.out_degree

    def serialize_vertex(self) -> dict:
        """This functions gets the state of the vertex in the form of a dictionary

        :return: dict
        """
        data = dict()
        data["data"], data["in_degree"], data["out_degree"] = self.get_state()
        return data


class Graph:
    def __init__(self, list_of_vertices: List[Any], list_of_edges: List[Tuple]) -> None:
        """This constructor initialized the graph object

        param
            list_of_vertices: list of vertices in the graph
            list_of_edges: list of edges in the graph

        :return: None
        """
        self.vertices = dict()
        self.graph = dict()
        self.vertex_count = 0
        self.edge_count = 0

        # intialize vertices and graph dictionaries
        for vertex in list_of_vertices:
            self.vertices[vertex] = Vertex(vertex)
            self.graph[vertex] = list()
            self.vertex_count += 1

        # intialize the graph
        for source_vertex, target_vertex in list_of_edges:
            # update the adjacency list
            self.graph[source_vertex].append(target_vertex)

            # update the internal state of the vertex
            self.vertices[source_vertex].increment_out_degree()
            self.vertices[target_vertex].increment_in_degree()

            # increment edge count
            self.edge_count += 1

    def count_edges(self) -> int:
        """This function returns the edge count of the graph

        :return: edge_count
        """
        return self.edge_count

    def count_vertices(self) -> int:
        """This function returns the vertex count of the graph

        :return: vertex_count
        """
        return self.vertex_count

    def serialize_graph(self) -> str:
        """This function returns the serialized graph

        :return: str
        """
        data = dict()
        data["vertices"] = dict()

        # serialize internal state of vertices
        for name, vertex in self.vertices.items():
            data["vertices"][name] = vertex.serialize_vertex()

        data["graph"] = self.graph

        return json.dumps(data, indent=4, sort_keys=True)

    def deserialize_graph(self, json_data: str) -> None:
        """This function takes the serialized graph and updates the graph state with it

        param
            json_data: the serialized graph

        :return: None
        """
        data = json.loads(json_data)
        self.graph = data["graph"]

        for name, vertex in data["vertices"].items():
            self.vertices[name] = Vertex(
                vertex["data"],
                vertex["in_degree"],
                vertex["out_degree"],
            )

    def get_histograms(self) -> Tuple[Counter, Counter]:
        """This function returns the histogram of the in degree and out degree for all the vertices

        :return: Counter, Counter
        """
        count_in_degree = [vertex.get_state()[1] for vertex in self.vertices.values()]
        count_out_degree = [vertex.get_state()[1] for vertex in self.vertices.values()]

        return Counter(count_in_degree), Counter(count_out_degree)

    def export_histogram(self, export_path: str) -> None:
        """This function export the histogram of the in degree and out degree
        for all the vertices in PNG format

        param
            export_path: the path of the directory where the image should be exported

        :return: None
        """
        count_in_degree, count_out_degree = self.get_histograms()
        plt.figure(figsize=(12, 9))
        ax = plt.subplot(111)

        # Remove ticks and spines
        ax.tick_params(left=False, bottom=False)
        for ax, spine in ax.spines.items():
            spine.set_visible(False)

        x1, x2 = np.array(list(count_in_degree.keys())), np.array(list(count_out_degree.keys()))
        y1, y2 = np.array(list(count_in_degree.values())), np.array(list(count_out_degree.values()))

        xs, ys = np.concatenate([x1, x2]), np.concatenate([y1, y2])
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        xstep, ystep = 1, 1

        # Limit the range of the plot to only where the data is.
        # Avoid unnecessary whitespace.
        plt.ylim(ymin - 1, ymax + 1)
        plt.xlim(xmin - 1, xmax + 1)

        plt.yticks(range(ymin - 1, ymax + 2, ystep), [str(x) for x in range(ymin - 1, ymax + 2, ystep)], fontsize=14)
        plt.xticks(range(xmin - 1, xmax + 2, xstep), [str(x) for x in range(xmin - 1, xmax + 2, xstep)], fontsize=14)

        for y in range(ymin - 1, ymax + 2, ystep):
            plt.plot(range(xmin - 1, xmax + 2), [y] * len(range(xmin - 1, xmax + 2)), "--", lw=0.5, color="black",
                     alpha=0.3)

        plt.title('Degree Distribution', fontsize=18)
        plt.xlabel('Degree', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)

        plt.bar(x=x1 - 0.1, height=y1, width=0.2, label="In Degree", bottom=None, align='center', data=None)
        plt.bar(x=x2 + 0.1, height=y2, width=0.2, label="Out Degree", bottom=None, align='center', data=None)
        plt.legend(borderpad=0.5, fontsize=10)
        plt.savefig(os.path.join(export_path, "Histogram.png"), bbox_inches="tight")
