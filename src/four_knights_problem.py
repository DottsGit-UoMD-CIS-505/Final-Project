"""
CIS 505 - Algorithm Design and Analysis
Final Project
Author: Nicholas Butzke

Program compares the effectiveness of the A* search algorithm
to that of branch and bound search.
Basic environment is a simplified version of the Four Knights Puzzle
|B . B             W . W
|. . .     ->      . . .
|W . W             B . B
"""

import sys
import time
from setup_board import setup_board
from a_star import a_star
from branch_and_bound import bnb
from node import Node


def print_path(node_list: list[Node]):
    """
    Takes a list of nodes and prints out the board_states using the print_board() method
    Arg1: a list of Node types

    Return: Nothing
    """
    for node in node_list:
        node.board.print_board()


def main():
    """
    Main wrapper function
    """
    # setup boards.  Start is default.  Goal is explicit here
    start_state, goal_state = setup_board(1)
    if len(sys.argv) == 2:
        if sys.argv[1] == "-a":
            # run only astar search
            print("not implemented")
        elif sys.argv[1] == "-b":
            # run only branch and bound search
            print("not implemented")
        else:
            print("Invalid arguments")
    else:
        # run both and compare

        # run and print A*
        start_time = time.time()
        a_star_path = a_star(start_state, goal_state)
        a_star_time = time.time() - start_time
        if isinstance(a_star_path, str):
            print(a_star_path)
        else:
            print(
                f"A* Solution: ({len(a_star_path) - 1} moves!) (Runtime: {a_star_time:.5f} s)"
            )
            print_path(a_star_path)

        # run and print Branch and Bound
        start_time = time.time()
        bnb_path = bnb(start_state, goal_state)
        bnb_time = time.time() - start_time
        if isinstance(bnb_path, str):
            print(bnb_path)
        else:
            print(
                f"Branch and Bound Solution: ({len(bnb_path) - 1} moves!) (Runtime: {bnb_time:.5f} s)"
            )
            print_path(bnb_path)

        move_dif = abs(len(a_star_path) - len(bnb_path))
        if len(a_star_path) > len(bnb_path):
            print(f"Branch and Bound path wins by {move_dif} moves!")
        elif len(a_star_path) < len(bnb_path):
            print(f"A* path wins by {move_dif} moves!")
        else:
            print("Equally optimal paths found by both algorithms!")


if __name__ == "__main__":
    main()
