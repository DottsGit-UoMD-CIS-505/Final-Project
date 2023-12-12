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
        board_choice = 3
        if board_choice == 1:
            start_board = [["B", ".", "B"], [".", ".", "."], ["W", ".", "W"]]
            start_white_pos = [[2, 0], [2, 2]]
            start_black_pos = [[0, 0], [0, 2]]
            start_state = Node(
                current_board=ChessBoard(
                    start_board, "W", start_white_pos, start_black_pos
                )
            )

            goal_board = [["W", ".", "W"], [".", ".", "."], ["B", ".", "B"]]
            goal_white_pos = [[0, 0], [0, 2]]
            goal_black_pos = [[2, 0], [2, 2]]
            goal_state = Node(
                current_board=ChessBoard(
                    goal_board, "W", goal_white_pos, goal_black_pos
                )
            )
        elif board_choice == 2:
            start_board = [
                ["B", ".", ".", "B"],
                [".", ".", ".", "."],
                [".", ".", ".", "."],
                ["W", ".", ".", "W"],
            ]
            start_white_pos = [[3, 0], [3, 3]]
            start_black_pos = [[0, 0], [0, 3]]
            start_state = Node(
                current_board=ChessBoard(
                    start_board, "W", start_white_pos, start_black_pos
                )
            )

            goal_board = [
                ["W", ".", ".", "W"],
                [".", ".", ".", "."],
                [".", ".", ".", "."],
                ["B", ".", ".", "B"],
            ]
            goal_white_pos = [[0, 0], [0, 3]]
            goal_black_pos = [[3, 0], [3, 3]]
            goal_state = Node(
                current_board=ChessBoard(
                    goal_board, "W", goal_white_pos, goal_black_pos
                )
            )
        elif board_choice == 3:
            start_board = [
                ["B", ".", ".", ".", "B"],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                ["W", ".", ".", ".", "W"],
            ]
            start_white_pos = [[4, 0], [4, 4]]
            start_black_pos = [[0, 0], [0, 4]]
            start_state = Node(
                current_board=ChessBoard(
                    start_board, "W", start_white_pos, start_black_pos
                )
            )

            goal_board = [
                ["W", ".", ".", ".", "W"],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                ["B", ".", ".", ".", "B"],
            ]
            goal_white_pos = [[0, 0], [0, 4]]
            goal_black_pos = [[4, 0], [4, 4]]
            goal_state = Node(
                current_board=ChessBoard(
                    goal_board, "W", goal_white_pos, goal_black_pos
                )
            )

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
        bnb_path = bnb(goal_state)
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
