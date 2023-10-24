"""
Function to check if the given object is in the given list.

Author: Nicholas Butzke
"""


def find(obj, lst: list):
    """
    Function to check if the given object is in the given list.
    Arg1: List (likely of Nodes)                                        |   []
    Arg2: Any (likely a Node)                                           |   Any

    Return: index of the object found.  If object not found returns -1  |   #

    Probably a built-in for this but I don't want to bother
    """
    try:
        return lst.index(obj)
    except ValueError:
        return -1
