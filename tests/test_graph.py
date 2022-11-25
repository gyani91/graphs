import json

from ..lib.graph import Graph
from ..test_data.lists import (
    TEST_LIST_OF_VERTICES,
    TEST_LIST_OF_EDGES,
    TEST_GRAPH,
    TEST_COUNT_IN_DEGREE,
    TEST_COUNT_OUT_DEGREE,
)

SERIALIZED_GRAPH_PATH = "test_data/graph.json"


def test_graph_creation():
    graph_obj = Graph(TEST_LIST_OF_VERTICES, TEST_LIST_OF_EDGES)
    assert graph_obj.graph == TEST_GRAPH


def test_serialize_graph():
    with open(SERIALIZED_GRAPH_PATH) as file:
        graph = json.load(file)

    graph_obj = Graph(TEST_LIST_OF_VERTICES, TEST_LIST_OF_EDGES)
    assert json.dumps(graph, indent=4, sort_keys=True) == graph_obj.serialize_graph()


def test_deserialize_graph():
    with open(SERIALIZED_GRAPH_PATH) as file:
        graph_json = json.dumps(json.load(file), indent=4, sort_keys=True)

    graph_obj_1 = Graph(TEST_LIST_OF_VERTICES, TEST_LIST_OF_EDGES)

    graph_obj_2 = Graph([], [])
    graph_obj_2.deserialize_graph(graph_json)

    assert graph_obj_1.vertices.keys() == graph_obj_2.vertices.keys()
    assert graph_obj_1.graph == graph_obj_2.graph


def test_get_histograms():
    graph_obj = Graph(TEST_LIST_OF_VERTICES, TEST_LIST_OF_EDGES)
    count_in_degree, count_out_degree = graph_obj.get_histograms()

    assert count_in_degree == TEST_COUNT_IN_DEGREE
    assert count_out_degree == TEST_COUNT_OUT_DEGREE
