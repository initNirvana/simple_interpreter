#


# r/Python based simple interpreter
# 단순한 스택 머신임 
from __future__ import print_function
from collections import deque

class Stack(deque):
    push = deque.append

    def top(self):
        return self[-1]

class Machine(object):
    def __init__(self, code):
        self.data_stack = Stack()
        self.return_addr_stack = Stack()
        self.instruction_pointer = 0
        self.code = code
