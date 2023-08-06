#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Stack
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/05/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Stack data structure. It is an iterable data
# structure where items can be added (push) and removed (pop). Items are added
# to the top of the stack but, items can be removed from anywhere within the 
# stack.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# get                         Returns the stack collection
# length                      Returns the number of items in the stack
# is_empty                    Verifies if the stack is empty, or not
# push                        Adds an item to the top of the stack
# pop                         Pops off an item from the stack
#*****************************************************************************
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

list

class Stack:
    """
    An iterable data structure or collection that may contain multiple data types.
    If no argument is given, the constructor creates a new empty stack.
    """

    def __init__(self, collection=[]):
        self._stack = collection
    
    def get(self) -> list:
        """
        This method is used to return the stack.

        Returns:
            list: Stack containing all data.
        """
        return self._stack
    
    def length(self) -> int:
        """
        This method is used to get the length of the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self._stack)
    
    def is_empty(self) -> bool:
        """
        This method is used to check whether the stack is empty or not.

        Returns:
            bool: True if the stack is empty. Otherwise, false.
        """
        if self._stack == []:
            return True
        else:
            return False

    def push(self, val: T) -> None:
        """
        This method is used to push items to the top of the stack.

        Args:
            val (T): An item of any data type.
        """
        self._stack.append(val)
    
    def pop(self, idx=-1) -> T:
        """
        This method is used to pop an item off of the stack.
        If no argument is given, the method will pop and return the top item.

        Args:
            idx (int, optional): The index of the item to be popped. Defaults to -1.

        Raises:
            IndexError: Raised when the given index is out of range.

        Returns:
            T: The popped item.
        """
        minimum = -len(self._stack) - 1
        maximum = len(self._stack) -1

        if (idx < minimum) or (idx > maximum):
            raise IndexError('Stack index out of range')

        item = self._stack[idx]
        if idx == 0:
            self._stack = self._stack[1:]
        elif idx == -1:
            self._stack = self._stack[:-1]
        elif idx > 0:
            self._stack = self._stack[:idx] + self._stack[idx + 1:]
        elif idx < 0:
            self._stack = self._stack[:idx] + self._stack[idx + 1:]

        return item