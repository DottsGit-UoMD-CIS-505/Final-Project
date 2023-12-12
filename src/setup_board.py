import random
from node import Node
from chess_board import ChessBoard


def setup_board(board_choice: int):
    if board_choice == 1:
        start_board = [["B", ".", "B"], [".", ".", "."], ["W", ".", "W"]]
        start_white_pos = [[2, 0], [2, 2]]
        start_black_pos = [[0, 0], [0, 2]]
        start_state = Node(
            current_board=ChessBoard(start_board, "W", start_white_pos, start_black_pos)
        )
        goal_board = [["W", ".", "W"], [".", ".", "."], ["B", ".", "B"]]
        goal_white_pos = [[0, 0], [0, 2]]
        goal_black_pos = [[2, 0], [2, 2]]
        goal_state = Node(
            current_board=ChessBoard(goal_board, "W", goal_white_pos, goal_black_pos)
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
            current_board=ChessBoard(start_board, "W", start_white_pos, start_black_pos)
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
            current_board=ChessBoard(goal_board, "W", goal_white_pos, goal_black_pos)
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
            current_board=ChessBoard(start_board, "W", start_white_pos, start_black_pos)
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
            current_board=ChessBoard(goal_board, "W", goal_white_pos, goal_black_pos)
        )
    if board_choice == 4:
        # procedurally generate knight placement on a 5x5 board
        start_board = [
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
        ]
        goal_board = [
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
        ]

        start_white_pos = []
        start_black_pos = []
        for i in range(0, 4):
            new_position = [random.randint(0, 4), random.randint(0, 4)]
            while new_position in start_white_pos or new_position in start_black_pos:
                new_position = [random.randint(0, 4), random.randint(0, 4)]
            if i < 2:
                start_white_pos.append(new_position)
            else:
                start_black_pos.append(new_position)
        goal_white_pos = start_black_pos
        goal_black_pos = start_white_pos

        # setup start board
        for pos in start_white_pos:
            start_board[pos[0]][pos[1]] = "W"
        for pos in start_black_pos:
            start_board[pos[0]][pos[1]] = "B"

        # setup goal board
        for pos in goal_white_pos:
            goal_board[pos[0]][pos[1]] = "W"
        for pos in goal_black_pos:
            goal_board[pos[0]][pos[1]] = "B"

        # create state objects
        start_state = Node(
            current_board=ChessBoard(start_board, "W", start_white_pos, start_black_pos)
        )
        goal_state = Node(
            current_board=ChessBoard(goal_board, "W", goal_white_pos, goal_black_pos)
        )
    return start_state, goal_state
