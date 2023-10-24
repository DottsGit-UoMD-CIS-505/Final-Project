"""
Chess board class that defaults to a 3x3 board

Author: Nicholas Butzke
"""

from copy import deepcopy


class ChessBoard:
    """
    Board state or node object.
    """

    def __init__(
        self,
        board_state=[["B", ".", "B"], [".", ".", "."], ["W", ".", "W"]],
        current_turn="W",
        white_kight_pos=[[2, 0], [2, 2]],
        black_knight_pos=[[0, 0], [0, 2]],
    ):
        self.board_state = board_state
        self.current_turn = current_turn  # white is W and black is B

        # Stores a list of knights and their positions.
        # Prevents searching for each knight on the board when calculating heuristic
        self.white_knight_pos = white_kight_pos
        self.black_knight_pos = black_knight_pos

    def get_piece(self, pos):
        """
        Method to return what piece is at a given position
        Mostly a supporter method of move_piece()
        Arg1: coordinate position to look for a piece                   |           [#,#]

        Return: piece found                                             |           char
        """
        return self.board_state[pos[0]][pos[1]]

    def set_piece(self, pos, piece):
        """
        Method to set a given position to a specific piece
        Supporter method of move_piece()
        Arg1: coordinate position to be set to a given piece            |           [#,#]
        Arg2: piece to be set to a given coordinate position            |           char

        Return: Nothing
        """
        self.board_state[pos[0]][pos[1]] = piece

    def change_pos_record(self, piece, pos, dest):
        """
        Method to update the knights' position records
        Mostly a supporter method of move_piece()
        Arg1: piece being moved.
            Used to essentially check what turn it is to modify the right list | char
        Arg2: coordinate position of the piece being moved                     | [#,#]
        Arg3: coordinate position of the piece after it is moved               | [#,#]

        Return: Nothing

        I wanted to make this to optimize tracking the pieces but I don't know if
        I reasonably used this or if it really cut down on time.
        Designed this early and just built it in.
        """
        if piece == "B":
            if self.black_knight_pos[0] == pos:
                self.black_knight_pos[0] = dest
            else:
                self.black_knight_pos[1] = dest
        if piece == "W":
            if self.white_knight_pos[0] == pos:
                self.white_knight_pos[0] = dest
            else:
                self.white_knight_pos[1] = dest

    def move_piece(self, piece_pos, piece_dest):
        """
        Method to move a piece at a given position to a given destination
        Arg1: coordinate position of the piece that needs to be moved          |        [#,#]
        Arg2: coordinate position of the piece after it is moved               |        [#,#]

        Return: Nothing
        """
        piece = self.get_piece(piece_pos)
        self.change_pos_record(piece, piece_pos, piece_dest)
        self.set_piece(piece_dest, piece)
        self.set_piece(piece_pos, ".")

    def print_board(self):
        """
        Method to print out the board

        Return: Nothing

        Mostly debugging.  Maybe some screenshots for documentation
        """
        for row in self.board_state:
            print(" ".join(row))
        print("_____")

    def __eq__(self, other):
        """
        Method to compare board states
        Compares both board state and who's turn it is
        to make sure the entire game is in the same state

        Return: if two boards are the same                                          |           Bool
        """
        return (
            self.board_state == other.board_state
            and self.current_turn == other.current_turn
        )


class Node:
    """
    Stores a ChessBoard and comparative information for heuristics and tree links
    Attributes:
        board
        g_score
        h_score
        f_score
        parent
        children
    Methods:
        check_valid_moves()
        get_knights_moves()
        calc_heuristic()
        make_child()
        make_children()
    """

    def __init__(self, current_board=ChessBoard(), g_score=0, h_score=0, parent=None):
        self.board = current_board
        self.g_score = g_score  # Cost from the start node
        self.h_score = h_score  # Heuristic estimate to the goal node
        self.f_score = g_score + h_score  # Total cost estimate
        self.parent = parent  # Reference to the parent node
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
            return self.board.white_knight_pos, [
                self.check_valid_moves(self.board.white_knight_pos[0]),
                self.check_valid_moves(self.board.white_knight_pos[1]),
            ]
        else:
            # black
            return self.board.black_knight_pos, [
                self.check_valid_moves(self.board.black_knight_pos[0]),
                self.check_valid_moves(self.board.black_knight_pos[1]),
            ]

    def calc_heuristic(self) -> None:
        """
        Calculates the weight of the predicted path
        """
        white_h = 0
        black_h = 0
        for white_knight in self.board.white_knight_pos:
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
            white_h += abs(d1 - 4) + abs(d2 - 4)

        for black_knight in self.board.black_knight_pos:
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
            black_h += abs(d1 - 4) + abs(d2 - 4)
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
            deepcopy(self.board.white_knight_pos),
            deepcopy(self.board.black_knight_pos),
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
