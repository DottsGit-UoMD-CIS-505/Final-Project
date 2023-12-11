"""
Chess board class that defaults to a 3x3 board

Author: Nicholas Butzke
"""


class ChessBoard:
    """
    Board state or node object.
    """

    def __init__(
        self,
        board_state=None,
        current_turn="W",
        white_kight_pos_list=None,
        black_knight_pos_list=None,
    ):
        if board_state is None:
            board_state = [["B", ".", "B"], [".", ".", "."], ["W", ".", "W"]]
        self.board_state = board_state
        self.current_turn = current_turn  # white is W and black is B

        # Stores a list of knights and their positions.
        # Prevents searching for each knight on the board when calculating heuristic
        if white_kight_pos_list is None:
            white_kight_pos_list = [[2, 0], [2, 2]]
        if black_knight_pos_list is None:
            black_knight_pos_list = [[0, 0], [0, 2]]
        self.white_knight_pos_list = white_kight_pos_list
        self.black_knight_pos_list = black_knight_pos_list

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
            if self.black_knight_pos_list[0] == pos:
                self.black_knight_pos_list[0] = dest
            else:
                self.black_knight_pos_list[1] = dest
        if piece == "W":
            if self.white_knight_pos_list[0] == pos:
                self.white_knight_pos_list[0] = dest
            else:
                self.white_knight_pos_list[1] = dest

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
