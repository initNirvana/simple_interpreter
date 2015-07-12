#!usr/bin/python

# r/Python based simple interpreter
# 단순한 스택 머신임 , 2 or 3 호환
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

    def pop(self):
        return self.data_stack.pop()
    def push(self, value):
        self.data_stack.push(value)
    def top(self):
        return self.data_stack.top()

    def run(self):
        while self.instrunction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)

    def dispatch(self, op):
        dispatch_map = {
            "%": self.mod,
            "*": self.mul,
            "+": self.plus,
            "/": self.div,
            "==": self.eq,
            "cast_int": self.cast_int,
            "cast_str": self.cast_str,
            "drop" : self.drop,
            "dup" : self.dup,
            "if" : self.if_stmt,
            "jmp" : self.jmp,
            "over" : self.over,
            "print": self.print_,
            "println" : self.println,
            "read": self.read,
            "stack": self.dump_stack,
            "swap": self.swap,
        }

        if op in dispatch_map:
            dispatch_map[op]()
        elif isinstance(op, int):
            self.push(op)
        elif isinstance(op, str) and op[0] == op[-1]=='"':
            self.push(op[1:-1])
        else:
            raise RuntimeError("Unknown opcode : '%s'"% op)
