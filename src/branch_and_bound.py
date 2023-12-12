"""
Branch and Bound algorithm that calculates the optimal path from source to destination.
This Branch and Bound is an exact Branch and Bound not a greedy Branch and Bound.

Author: Nicholas Butzke
"""

from find import find
from node import Node
import heapq


def bnb(start_state: Node, goal_state: Node):
    """
    Branch and Bound Algorithm
    Finds the shortest path from a source to a destination using traditional methods
    Arg1: destination node                                                           |    Node

    Return: Optimal path if one is found. Otherwise will report no path found        |    list[Node]
    """
    open_heap: heapq = []
    heapq.heappush(open_heap, (0, start_state))
    open_set: set[Node] = set()
    open_set.add(start_state)
    closed_set: set[Node] = set()

    shortest_path = []
    shortest_path_length = float("inf")  # this is the bound
    while open_set:
        current_node: Node
        _, current_node = heapq.heappop(open_heap)
        open_set.remove(current_node)
        # Report if the front of the queue is the goal
        if current_node.board.board_state == goal_state.board.board_state:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = current_node.parent
            if len(path) <= shortest_path_length:
                shortest_path_length = len(path)
            shortest_path = path[::-1]
        else:  # Didn't find the goal
            if current_node.g_score + 1 < shortest_path_length:
                current_node.make_children()  # Generate its children nodes
                for child in current_node.children:
                    if not (child in open_set and child.g_score < shortest_path_length):
                        # Look if an equivilant to the child node has already been checked
                        if child not in closed_set:
                            heapq.heappush(open_heap, (child.g_score, child))
                            open_set.add(child)
        closed_set.add(current_node)
    if shortest_path:
        return shortest_path
    return "no path found"
