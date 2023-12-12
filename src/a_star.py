"""
A* algorithm that calculates the optimal path from source to destination.

Author: Nicholas Butzke
"""

from node import Node
from find import find


def a_star(start_state: Node, goal_state: Node):
    """
    A* Algorithm
    Finds the shortest path from a source to a destination using heuristics
    Arg1: destination node                                                    | Node

    Return: Optimal path if one is found. Otherwise will report no path found | list[Node]
    """
    open_list: list[Node] = [start_state]
    closed_list: list[Node] = []
    while open_list:
        current_node = min(open_list, key=lambda node: node.f_score)
        open_list.remove(current_node)
        current_node.make_children()
        for child in current_node.children:
            if child.board.board_state == goal_state.board.board_state:
                optimal_path = [goal_state]
                while current_node is not None:
                    optimal_path.append(current_node)
                    current_node = current_node.parent
                print(f"Closed List Length: {len(closed_list)}")
                return optimal_path[::-1]
            child.calc_heuristic(goal_state.board)
            # child.calc_heuristic_old()
            i = find(child, open_list)
            if not (i != -1 and open_list[i].f_score < child.f_score):
                i = find(child, closed_list)
                if not (i != -1 and closed_list[i].f_score < child.f_score):
                    open_list.append(child)
        closed_list.append(current_node)
    return "no path found"
