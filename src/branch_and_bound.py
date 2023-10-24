"""
Branch and Bound algorithm that calculates the optimal path from source to destination.

Author: Nicholas Butzke
"""

from find import find
from chess_board import Node


def bnb(goal_state: Node):
    """
    Branch and Bound Algorithm
    Finds the shortest path from a source to a destination using traditional methods
    Arg1: destination node                                                           |    Node

    Return: Optimal path if one is found. Otherwise will report no path found        |    list[Node]
    """
    open_list: list[Node] = [Node()]
    closed_list: list[Node] = []
    shortest_path = []
    shortest_path_length = float("inf")
    while open_list:
        current_node = open_list.pop(0)
        if (
            current_node.board.board_state == goal_state.board.board_state
        ):  # Report if the front of the queue is the goal
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
                    i = find(
                        child, open_list
                    )  # Look if a child node is already in the queue
                    if i == -1 and child.g_score < shortest_path_length:
                        i = find(
                            child, closed_list
                        )  # Look if an equivilant to the child node has already been checked
                        if i == -1:
                            open_list = [
                                child
                            ] + open_list  # If node is novel add it to the front of the queue
        if open_list:
            m_node = min(
                open_list, key=lambda node: node.g_score
            )  # Find node with minimum spent cost (g)
            if (
                m_node != open_list[0]
            ):  # If not with minimum g is not at the front of the queue, put it there
                open_list.remove(m_node)
                open_list = [m_node] + open_list
        closed_list.append(current_node)
    if shortest_path:
        return shortest_path
    else:
        return "no path found"
