import math
from typing import List, Tuple
import numpy as np


def points_to_graph(points: List[Tuple[int, int]]) -> np.ndarray:
    distances = [((i, j), math.dist(points[i], points[j]))
                 for i in range(points) for j in range(i)]
    graph = [[distances[max(i, j) * len(points) + min(i, j)] for j in range(len(points))]
             for i in range(len(points))]
    return np.array(graph)


def shortest_path(start_pos: int, end_pos: int, adj_matrix: np.ndarray) -> List[int]:
    backtrace = simple_dijkstra(adj_matrix, start_pos)
    return unroll_shortest_path(start_pos, end_pos, backtrace)


def unroll_shortest_path(start_pos: int, end_pos: int, backtrace: List[int]) -> List[int]:
    path = [end_pos]
    pos = end_pos

    while pos != start_pos:
        pos = backtrace[pos]
        if pos == -1:
            return [start_pos]
        path.insert(0, pos)

    return path


def simple_dijkstra(adj_matrix: np.ndarray, start_node: int) -> List[int]:
    num_nodes = adj_matrix.shape[0]
    dist = np.full((num_nodes), np.inf, dtype=np.float32)
    backtrace = np.full((num_nodes,), -1, dtype=np.int32)

    dist[start_node] = 0.0
    unvisited_nodes = list(range(num_nodes))

    while unvisited_nodes:
        dist_in_queue = dist[unvisited_nodes]
        node_to_visit = unvisited_nodes[np.argmin(dist_in_queue)]

        if dist[node_to_visit] == np.inf:
            break

        conn_nodes = [i for i in list(range(num_nodes)) if adj_matrix[node_to_visit][i]]

        for index in conn_nodes:
            new_dist = dist[node_to_visit] + adj_matrix[node_to_visit][index]
            if new_dist < dist[index]:
                dist[index] = new_dist
                backtrace[index] = node_to_visit

        unvisited_nodes.remove(node_to_visit)

    return backtrace.tolist()
