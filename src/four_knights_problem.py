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
from chess_board import ChessBoard
from a_star import a_star
from branch_and_bound import bnb


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

        # setup boards.  Start is default.  Goal is explicit here
        goal_board = [["W", ".", "W"], [".", ".", "."], ["B", ".", "B"]]
        goal_state = Node(current_board=ChessBoard(goal_board))

        # run and print A*
        start_time = time.time()
        a_star_path = a_star(goal_state)
        a_star_time = time.time() - start_time
        print(
            "A* Solution: ("
            + str(len(a_star_path) - 1)
            + " moves!) (Runtime: "
            + format(a_star_time, ".5f")
            + "s)"
        )
        print_path(a_star_path)

        # run and print Branch and Bound
        start_time = time.time()
        bnb_path = bnb(goal_state)
        bnb_time = time.time() - start_time
        print(
            "Branch and Bound Solution: ("
            + str(len(bnb_path) - 1)
            + " moves!) (Runtime: "
            + format(bnb_time, ".5f")
            + "s)"
        )
        print_path(bnb_path)

        move_dif = abs(len(a_star_path) - len(bnb_path))
        if len(a_star_path) > len(bnb_path):
            print("Branch and Bound path wins by " + str(move_dif) + " moves!")
        elif len(a_star_path) < len(bnb_path):
            print("A* path wins by " + str(move_dif) + " moves!")
        else:
            print("Equally optimal paths found by both algorithms!")


if __name__ == "__main__":
    main()
