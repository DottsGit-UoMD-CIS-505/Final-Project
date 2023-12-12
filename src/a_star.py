"""
A* algorithm that calculates the optimal path from source to destination.

Author: Nicholas Butzke
"""

from node import Node
from find import find
import heapq


def a_star(start_state: Node, goal_state: Node):
    """
    A* Algorithm
    Finds the shortest path from a source to a destination using heuristics
    Arg1: destination node                                                    | Node

    Return: Optimal path if one is found. Otherwise will report no path found | list[Node]
    """
    open_heap: heapq = []
    heapq.heappush(open_heap, (0, start_state))
    open_set: set[Node] = set()
    open_set.add(start_state)
    closed_set: set[Node] = set()
    while open_heap:
        # current_node = min(open_list, key=lambda node: node.f_score)
        current_node: Node
        _, current_node = heapq.heappop(open_heap)
        open_set.remove(current_node)
        current_node.make_children()
        for child in current_node.children:
            if child.board.board_state == goal_state.board.board_state:
                optimal_path = [goal_state]
                while current_node is not None:
                    optimal_path.append(current_node)
                    current_node = current_node.parent
                print(f"Closed List Length: {len(closed_set)}")
                return optimal_path[::-1]
            child.calc_heuristic(goal_state.board)
            # child.calc_heuristic_old()
            if child not in open_set:
                if child not in closed_set:
                    heapq.heappush(open_heap, (child.f_score, child))
                    open_set.add(child)
        closed_set.add(current_node)
    return "no path found"
