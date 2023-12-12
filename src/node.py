"""
Node class for constructing a tree

Author: Nicholas Butzke
"""

from copy import deepcopy
from math import inf
from math import floor
from chess_board import ChessBoard


class Node:
    """
    Stores a ChessBoard and comparative information for heuristics and tree links
    Attributes:
        board (ChessBoard): Stores the board state for the current node
        g_score (int): Stores the cost from the start to the current state
        h_score (int): Stores the predicted cost from the current state to the target state
        f_score (int): Stores the sum of g and h
        parent (Node): Stores the preceding Node
        children (list[Node]): Stores Nodes that represent potential next moves
    Methods:
        check_valid_moves(knight_pos)
        get_knights_moves()
        calc_heuristic()
        make_child(pos, dest)
        make_children()
    """

    def __init__(self, current_board=ChessBoard(), g_score=0, h_score=0, parent=None):
        self.board: ChessBoard = current_board
        self.g_score: int = g_score  # Cost from the start node
        self.h_score: int = h_score  # Heuristic estimate to the goal node
        self.f_score: int = g_score + h_score  # Total cost estimate
        self.parent: Node = parent  # Reference to the parent node
        self.children: list[Node] = []

    def check_valid_moves(self, knight_pos):
        """
        Finds valid moves of a SINGLE knight
        Supporter method for get_knights_moves()
        Arg1: coordinate position of a knight                  | [#,#]

        Return: list of valid destination coordinate positions | [[#,#],[#,#],...[#,#]]
        """
        moves = []
        possible_moves = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]  # relative
        for p_move in possible_moves:
            n_row, n_col = knight_pos[0] + p_move[0], knight_pos[1] + p_move[1]
            if (
                (n_row >= 0 and n_row <= 2)
                and (n_col >= 0 and n_col <= 2)
                and self.board.get_piece([n_row, n_col])
            ) == ".":
                moves.append((n_row, n_col))
        return moves

    def get_knights_moves(self):
        """
        Finds moves for both knights for whoever's turn it is
        Return: source and destination parallel lists         ->    source, destination

        Source is a list of coordinate positions for both
        knights from the white/black class attribute          | [[#,#],[#,#]]

        Destination a list of destination coordinate
        positions for both knights -> [a,b]
            [[[#,#],[#,#],...[#,#]] , [[#,#],[#,#],...[#,#]]]
        notice the seperation here ⤴

        'a' is a list of all positions the first knight can move to
        'b' is a list of all positions the second knight can move to
        """
        if self.board.current_turn == "W":
            # white
            return self.board.white_knight_pos_list, [
                self.check_valid_moves(self.board.white_knight_pos_list[0]),
                self.check_valid_moves(self.board.white_knight_pos_list[1]),
            ]
        else:
            # black
            return self.board.black_knight_pos_list, [
                self.check_valid_moves(self.board.black_knight_pos_list[0]),
                self.check_valid_moves(self.board.black_knight_pos_list[1]),
            ]

    def calc_heuristic(self, goal_board: ChessBoard) -> None:
        white_h = 0
        black_h = 0

        white_dest_list = goal_board.white_knight_pos_list
        black_dest_list = goal_board.black_knight_pos_list

        for white_knight in self.board.white_knight_pos_list:
            local_min_h = inf
            for dest in white_dest_list:
                distance = sum(abs(a - b) for a, b in zip(white_knight, dest))
                heuristic = floor(
                    ((2 / 3) * (distance - 3) * (distance - 2) - 1) * (distance - 1) + 3
                )
                if heuristic < local_min_h:
                    local_min_h = heuristic
            white_h += local_min_h
        for black_knight in self.board.black_knight_pos_list:
            local_min_h = inf
            for dest in black_dest_list:
                distance = sum(abs(a - b) for a, b in zip(black_knight, dest))
                heuristic = floor(
                    ((2 / 3) * (distance - 3) * (distance - 2) - 1) * (distance - 1) + 3
                )
                if heuristic < local_min_h:
                    local_min_h = heuristic
            black_h += local_min_h

        self.h_score = white_h + black_h
        self.f_score = self.g_score + self.h_score

    def calc_heuristic_old(self) -> None:
        """
        Calculates the weight of the predicted path
        """
        white_h = 0
        black_h = 0
        for white_knight in self.board.white_knight_pos_list:
            d1 = abs(white_knight[0] - 0) + abs(white_knight[1] - 0)
            d2 = abs(white_knight[0] - 0) + abs(white_knight[1] - 2)
            if d1 == 0:
                d1 = 4
            elif d1 == 4:
                d1 = 2
            if d2 == 0:
                d2 = 4
            elif d2 == 4:
                d2 = 2

            white_h += abs(d1 - 4) + abs(d2 - 4) + 1

        for black_knight in self.board.black_knight_pos_list:
            d1 = abs(black_knight[0] - 2) + abs(black_knight[1] - 0)
            d2 = abs(black_knight[0] - 2) + abs(black_knight[1] - 2)
            if d1 == 0:
                d1 = 4
            elif d1 == 4:
                d1 = 2
            if d2 == 0:
                d2 = 4
            elif d2 == 4:
                d2 = 2
            black_h += abs(d1 - 4) + abs(d2 - 4) + 1
        self.h_score = (white_h + black_h) * 2
        # Heavily weighting the predicted cost with *2 favors visited nodes
        # which are more likely to be closer to the destination neighboring nodes.
        # Makes runtime go from ~30s to nearly instantaneous
        self.f_score = self.g_score + self.h_score

    def make_child(self, pos, dest):
        """
        Method to make a child node
        Supports make_children()
        Arg1: coordinate position of piece that is about to be moved             | [#,#]
        Arg2: coordinate position of piece after it is moved                     | [#,#]

        Return: child node with an adjusted board_state, current_turn, and g_score | Node
        """
        if self.board.current_turn == "W":
            next_turn = "B"
        else:
            next_turn = "W"
        child_board = ChessBoard(
            deepcopy(self.board.board_state),
            next_turn,
            deepcopy(self.board.white_knight_pos_list),
            deepcopy(self.board.black_knight_pos_list),
        )
        child_board.move_piece(pos, dest)
        child = Node(child_board, self.g_score + 1, deepcopy(self.h_score), self)
        return child

    def make_children(self):
        """
        Makes a list of children

        Return: Nothing
        """
        pos_list, dest_list = self.get_knights_moves()
        for i, pos in enumerate(pos_list):
            for dest in dest_list[i]:
                self.children.append(self.make_child(pos, dest))

    def __eq__(self, other):
        """
        Method to compare board states
        """
        return self.board == other.board
