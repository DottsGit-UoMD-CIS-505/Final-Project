"""
CIS 579 - Artificial Intelligence
Assignemnt 1
Author: Nicholas Butzke

Program compares the effectiveness of the A* search algorithm to that of traditional branch and bound search.
Environment is a simplified version of the Four Knights Puzzle
|B . B             W . W
|. . .     ->      . . .
|W . W             B . B
"""

import sys
from copy import deepcopy
import time

class ChessBoard:
    def __init__(self, boardState=[['B', '.', 'B'],['.', '.', '.'],['W', '.', 'W']], currentTurn='W', whiteKightPos=[[2,0],[2,2]], blackKnightPos=[[0,0],[0,2]]):
        self.boardState = boardState
        self.currentTurn = currentTurn #white is W and black is B
        
        #Stores a list of knights and their positions. Prevents searching for each knight on the board when calculating heuristic
        self.whiteKnightPos = whiteKightPos
        self.blackKnightPos = blackKnightPos


    """
    Method to return what piece is at a given position
    Mostly a supporter method of move_piece()
    Arg1: coordinate position to look for a piece                   |           [#,#]

    Return: piece found                                             |           char
    """
    def get_piece(self, pos):
        return self.boardState[pos[0]][pos[1]]

    """
    Method to set a given position to a specific piece
    Supporter method of move_piece()
    Arg1: coordinate position to be set to a given piece            |           [#,#]
    Arg2: piece to be set to a given coordinate position            |           char

    Return: Nothing
    """
    def set_piece(self, pos, piece):
        self.boardState[pos[0]][pos[1]] = piece

    """
    Method to update the knights' position records
    Mostly a supporter method of move_piece()
    Arg1: piece being moved.  Used to essentially check what turn it is to modify the right list            |           char
    Arg2: coordinate position of the piece being moved                                                      |           [#,#]
    Arg3: coordinate position of the piece after it is moved                                                |           [#,#]

    Return: Nothing
    
    I wanted to make this to optimize tracking the pieces but I don't know if I reasonably used this or if it really cut down on time.
    Designed this early and just built it in.
    """
    def change_pos_record(self, piece, pos, dest):
        if piece == 'B':
            if self.blackKnightPos[0] == pos:
                self.blackKnightPos[0] = dest
            else:
                self.blackKnightPos[1] = dest
        if piece == 'W':
            if self.whiteKnightPos[0] == pos:
                self.whiteKnightPos[0] = dest
            else:
                self.whiteKnightPos[1] = dest

    """
    Method to move a piece at a given position to a given destination
    Arg1: coordinate position of the piece that needs to be moved               |           [#,#]
    Arg2: coordinate position of the piece after it is moved                    |           [#,#]

    Return: Nothing
    """
    def move_piece(self, piecePos, pieceDest):
        piece = self.get_piece(piecePos)
        self.change_pos_record(piece, piecePos, pieceDest)
        self.set_piece(pieceDest, piece)
        self.set_piece(piecePos, '.')

    """
    Method to print out the board

    Return: Nothing
    
    Mostly debugging.  Maybe some screenshots for documentation
    """
    def print_board(self):
        for row in self.boardState:
            print(' '.join(row))
        print("_____")
        
   
    """
    Method to compare board states
    Compares both board state and who's turn it is to make sure the entire game is in the same state

    Return: if two boards are the same                                          |           Bool
    """
    def __eq__(self, other):
        return self.boardState == other.boardState and self.currentTurn == other.currentTurn

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
class Node:
    def __init__(self, currentBoard=ChessBoard(), g_score=0, h_score=0, parent=None):
        self.board = currentBoard
        self.g_score = g_score  # Cost from the start node
        self.h_score = h_score  # Heuristic estimate to the goal node
        self.f_score = g_score + h_score  # Total cost estimate
        self.parent = parent  # Reference to the parent node
        self.children: list[Node] = []

    
    """
    Finds valid moves of a SINGLE knight
    Supporter method for get_knights_moves()
    Arg1: coordinate position of a knight                                       |           [#,#]

    Return: list of valid destination coordinate positions                      |           [[#,#],[#,#],...[#,#]]
    """
    def check_valid_moves(self, knightPos):
        moves = []
        possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)] #relative
        for pMove in possible_moves:
            nRow, nCol = knightPos[0] + pMove[0], knightPos[1] + pMove[1]
            if ((nRow >= 0 and nRow <= 2) and (nCol >= 0 and nCol <= 2) and self.board.get_piece([nRow, nCol])) == '.':
                moves.append((nRow, nCol))
        return moves
    
    """
    Finds moves for both knights for whoever's turn it is
    Return: source and destination parallel lists                                                            ->          source, destination
    
    Source is a list of coordinate positions for both knights from the white/black class attribute           |           [[#,#],[#,#]]

    Destination a list of destination coordinate positions for both knights -> [a,b]                         |           [[[#,#],[#,#],...[#,#]] , [[#,#],[#,#],...[#,#]]]
    'a' is a list of all positions the first knight can move to                                                      notice the seperation here ⤴
    'b' is a list of all positions the second knight can move to
    """
    def get_knights_moves(self):
        if self.board.currentTurn == 'W':
            #white
            return self.board.whiteKnightPos, [self.check_valid_moves(self.board.whiteKnightPos[0]), self.check_valid_moves(self.board.whiteKnightPos[1])]
        else:
            #black
            return self.board.blackKnightPos, [self.check_valid_moves(self.board.blackKnightPos[0]), self.check_valid_moves(self.board.blackKnightPos[1])]
    
    """
    Calculates predicted cost to a goal state
    
    Return: Nothing
    
    Probably a better way to do this as knights jump weird.  Being right next to the destination is WORSE than further (somtimes).  Maybe inverse?
    """
    """
    def old_calc_heuristic(self) -> None:
        #Heuristic will be calculated using the shortest distance to a destination point.  Subtracting zero is for sanity on where the destination is
        whiteHeuristic = 0
        blackHeuristic = 0
        for whiteKnight in self.board.whiteKnightPos:
            whiteHeuristic += min(abs(whiteKnight[0]-0) + abs(whiteKnight[1]-0), abs(whiteKnight[0]-0) + abs(whiteKnight[1]-2))
        for blackKnight in self.board.blackKnightPos:
            blackHeuristic += min(abs(blackKnight[0]-2) + abs(blackKnight[1]-0), abs(blackKnight[0]-2) + abs(blackKnight[1]-2))
        self.h_score = whiteHeuristic + blackHeuristic
        self.f_score = self.g_score + self.h_score
    """
    """
    def strict_calc_heuristic(self) -> None:
        whiteHeuristic = 0
        blackHeuristic = 0
        for whiteKnight in self.board.whiteKnightPos:
            whiteKnight = list(whiteKnight)
            if whiteKnight in [[0,0],[0,2]]:
                whiteHeuristic += 0
            elif whiteKnight in [[1,0],[1,2],[2,1]]:
                whiteHeuristic += 1
            elif whiteKnight in [[2,0],[2,2]]:
                whiteHeuristic += 2
            elif whiteKnight in [[0,1]]:
                whiteHeuristic += 3
            else:
                print("oof White")
                print(whiteKnight in [[0,0],[0,2]])
                print(whiteKnight)
                print(self.g_score)
                self.board.print_board()
                sys.exit(0)
        for blackKnight in self.board.blackKnightPos:
            blackKnight = list(blackKnight)
            if blackKnight in [[2,0],[2,2]]:
                blackHeuristic += 0
            elif blackKnight in [[1,0],[1,2],[0,1]]:
                blackHeuristic += 1
            elif blackKnight in [[0,0],[0,2]]:
                blackHeuristic += 2
            elif blackKnight in [[2,1]]:
                blackHeuristic += 3
            else:
                print("oof Black")
                print(blackKnight)
                self.board.print_board()
                sys.exit(0)
        self.h_score = whiteHeuristic + blackHeuristic
        self.f_score = self.g_score + self.h_score
    """
    def calc_heuristic(self) -> None:
        whiteH = 0
        blackH = 0
        for whiteKnight in self.board.whiteKnightPos:
            d1 = abs(whiteKnight[0]-0) + abs(whiteKnight[1]-0)
            d2 = abs(whiteKnight[0]-0) + abs(whiteKnight[1]-2)
            if d1 == 0:
                d1 = 4
            elif d1 == 4:
                d1 = 2
            if d2 == 0:
                d2 = 4
            elif d2 == 4:
                d2 = 2
            whiteH += abs(d1 - 4) + abs(d2 - 4)
        for blackKnight in self.board.blackKnightPos:
            d1 = abs(blackKnight[0]-2) + abs(blackKnight[1]-0)
            d2 = abs(blackKnight[0]-2) + abs(blackKnight[1]-2)
            if d1 == 0:
                d1 = 4
            elif d1 == 4:
                d1 = 2
            if d2 == 0:
                d2 = 4
            elif d2 == 4:
                d2 = 2
            blackH += abs(d1 - 4) + abs(d2 - 4)
        self.h_score = (whiteH + blackH)*2 #Heavily weighting the predicted cost with *2 favors visited nodes which are more likely to be closer to the destination neighboring nodes.  Makes runtime go from ~30s to nearly instantaneous
        self.f_score = self.g_score + self.h_score

    """
    Method to make a child node
    Supports make_children()
    Arg1: coordinate position of piece that is about to be moved                           |            [#,#]
    Arg2: coordinate position of piece after it is moved                                   |            [#,#]

    Return: child node with an adjusted boardState, currentTurn, and g_score               |            Node
    """
    def make_child(self, pos, dest):
        if self.board.currentTurn == 'W':
            nextTurn = 'B'
        else:
            nextTurn = 'W'
        childBoard = ChessBoard(deepcopy(self.board.boardState), nextTurn, deepcopy(self.board.whiteKnightPos), deepcopy(self.board.blackKnightPos))
        childBoard.move_piece(pos, dest)
        child = Node(childBoard, self.g_score + 1, deepcopy(self.h_score), self)
        return child
    
    """
    Makes a list of children

    Return: Nothing
    """
    def make_children(self):
        posList, destList = self.get_knights_moves()
        for i, pos in enumerate(posList):
            for dest in destList[i]:
                self.children.append(self.make_child(pos, dest))

    """
    Method to compare board states


    """
    def __eq__(self, other):
        return self.board == other.board

"""
Function to check if the given object is in the given list.
Arg1: List (likely of Nodes)                                                                         |           []
Arg2: Any (likely a Node)                                                                            |           Any

Return: index of the object found.  If object not found returns -1                                   |           #

Probably a built-in for this but I don't want to bother
"""
def find(obj, lst: list):
    try:
        return lst.index(obj)
    except ValueError:
        return -1

"""
A* Algorithm
Finds the shortest path from a source to a destination using heuristics
Arg1: destination node                                                                              |           Node

Return: Optimal path if one is found. Otherwise will report no path found                           |           list[Node]
"""
def aStar(goalState: Node):
    open_list: list[Node] = [Node()]
    closed_list: list[Node] = []
    while open_list:
        currentNode = min(open_list, key=lambda node: node.f_score)
        open_list.remove(currentNode)
        currentNode.make_children()
        for child in currentNode.children:
            if child.board.boardState == goalState.board.boardState:
                optimalPath = [goalState]
                while currentNode is not None:
                    optimalPath.append(currentNode)
                    currentNode = currentNode.parent
                return optimalPath[::-1]
            child.calc_heuristic()
            i = find(child, open_list)
            if not (i != -1 and open_list[i].f_score < child.f_score):
                i = find(child, closed_list)
                if not (i != -1 and closed_list[i].f_score < child.f_score):
                    open_list.append(child)
        closed_list.append(currentNode)
    return "no path found"

"""
Branch and Bound Algorithm
Finds the shortest path from a source to a destination using traditional methods
Arg1: destination node                                                                              |           Node

Return: Optimal path if one is found. Otherwise will report no path found                           |           list[Node]
"""
def bnb(goalState: Node):
    open_list: list[Node] = [Node()]
    closed_list: list[Node] = []
    shortestPath = []
    shortestPathLength = float('inf')
    while open_list:
        currentNode = open_list.pop(0)
        if currentNode.board.boardState == goalState.board.boardState:                                                   # Report if the front of the queue is the goal
            path = []
            while currentNode is not None:
                path.append(currentNode)
                currentNode = currentNode.parent
            if len(path) <= shortestPathLength:
                shortestPathLength = len(path)
            shortestPath = path[::-1]
        else:                                                                               # Didn't find the goal                                                 # Grab the front of the queue
            if currentNode.g_score + 1 < shortestPathLength:
                currentNode.make_children()                                                 # Generate its children nodes
                for child in currentNode.children:
                    i = find(child, open_list)                                              # Look if a child node is already in the queue
                    if i == -1 and child.g_score < shortestPathLength:
                        i = find(child, closed_list)                                        # Look if an equivilant to the child node has already been checked
                        if i == -1:
                            open_list = [child] + open_list                                 # If node is novel add it to the front of the queue
        if open_list:
            mNode = min(open_list, key=lambda node: node.g_score)                           # Find node with minimum spent cost (g)
            if mNode != open_list[0]:                                                       # If not with minimum g is not at the front of the queue, put it there
                open_list.remove(mNode) 
                open_list = [mNode] + open_list
        closed_list.append(currentNode)
    if shortestPath:
        return shortestPath
    else:
        return "no path found"

"""
Takes a list of nodes and prints out the boardstates using the print_board() method
Arg1: a list of Node types

Return: Nothing
"""
def print_path(nodeList: list[Node]):
    for node in nodeList:
        node.board.print_board()

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "-a":
            #run only astar search
            print("not implemented")
        elif sys.argv[1] == "-b":
            #run only branch and bound search
            print("not implemented")
        else:
            print("Invalid arguments")
    else:
        #run both and compare

        #setup boards.  Start is default.  Goal is explicit here
        goalBoard = [['W', '.', 'W'],
                     ['.', '.', '.'],
                     ['B', '.', 'B']]
        goalState = Node(currentBoard = ChessBoard(goalBoard))

        #run and print A*
        startTime = time.time()
        aStarPath = aStar(goalState)
        aStarTime = time.time() - startTime
        print("A* Solution: (" + str(len(aStarPath)-1) + " moves!) (Runtime: " + format(aStarTime, ".5f") + "s)")
        print_path(aStarPath)

        #run and print Branch and Bound
        startTime = time.time()
        bnbPath = bnb(goalState)
        bnbTime = time.time() - startTime
        print("Branch and Bound Solution: (" + str(len(bnbPath)-1) + " moves!) (Runtime: " + format(bnbTime, ".5f") + "s)")
        print_path(bnbPath)

        moveDif = abs(len(aStarPath) - len(bnbPath))
        if len(aStarPath) > len(bnbPath):
            print("Branch and Bound path wins by " + str(moveDif) + " moves!")
        elif len(aStarPath) < len(bnbPath):
            print("A* path wins by " + str(moveDif) + " moves!")
        else:
            print("Equally optimal paths found by both algorithms!")

if __name__ == "__main__":
    main()