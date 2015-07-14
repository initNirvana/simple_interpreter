# -*- coding:utf-8 -*-
#!usr/bin/python3
# r/Python based simple interpreter
# 단순한 스택 머신임 , 2 or 3 호환
from __future__ import print_function
from collections import deque
import sys
import tokenize
from StringIO import StringIO

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
        while self.instruction_pointer < len(self.code):
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

    def plus(self):
        self.push(self.pop() + self.pop())

    def minus(self):
        last = self.pop()
        self.push(self.pop() - last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)

    def mod(self):
        last = self.pop()
        self.push(self.pop() % last)

    def dup(self):
        self.push(self.top())

    def eq(self):
        self.push(str(self.pop()))

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

    def over(self):
        b = self.pop()
        a = self.pop()
        self.push(a)
        self.push(b)
        self.push(a)

    def drop(self):
        self.pop()

    def swap(self):
        b = self.pop()
        a = self.pop()
        self.push(b)
        self.push(a)

    def print_(self):
        sys.stdout.write(str(self.pop()))
        sys.stdout.flush()

    def println(self):
        sys.stdout.write("%s\n" % self.pop())
        sys.stdout.flush()

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)

    def jmp(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")

    def dump_stack(self):
        print("Data stack (top first):")

        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))

    def read(self):
        self.push(raw_input())

    def parse(text):
        tokens = tokenize.generate_tokens(StringIO(text).readline)
        for toknum, tokval, _, _, _ in tokens:
            if toknum == tokenize.NUMBER:
                yield int(tokval)
            elif toknum in [tokenize.OP, tokenize.STRING, tokenize.Name]:
                yield tokval
            elif toknum == tokenize.ENDMARKER
                break
            else:
                raise RuntimeError("Unknown token %s: '%s'" % tokenize.tok_name[toknum], tokval)

    def constant_fold(code):
        while True:
            for i, (a, b, op) in enumerate(zip(code, code[1:], code[2:])):
                if isinstance(a, int) and isinstance(b, int) and op in {"+", "-", "*", "/"}:
                    m = Machine((a,b,op))
                    m.run()
                    code[i:i+3] = [m.top()]
                    print("constant_fold %s%s%s to %s" % (a,op,b,m.top()))
                    break
                else:
                    break
        return code

    def repl()
        print("Ctrl("cmd")+D or type "exit" to quit.")

        while True:
            try:
                source = raw_input("> ")
                code = list(parse(source))
                code = constant_fold(code)
                Machine(code).run()
            except (RuntimeError, IndexError) as e:
                print("IndexError: %s" % e)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")

def test(code = [2, 3, "+", 5, "*", "println"]):
    print("Code before optimization: %s" % str(code))
    optimized = constant_fold(code)
    print("Code after optimization: %s" % str(optimized))

    print("Stack after running original program:")
    a = Machine(code)
    a.run()
    a.dump_stack()

    print("Stack after running optimized program:")
    b = Machine(optimized)
    b.run()
    b.dump_stack()

    result = a.data_stack == b.data_stack
    print("Result: %s" % ("OK" if result else "FAIL"))
    return result

def examples():
    print("** Program 1: Runs the code for `print((2+3)*4)`")
    Machine([2, 3, "+", 4, "*", "println"]).run()

    print("\n** Program 2: Ask for numbers, computes sum and product.")
    Machine([
        '"Enter a number: "', "print", "read", "cast_int",
        '"Enter another number: "', "print", "read", "cast_int",
        "over", "over",
        '"Their sum is: "', "print", "+", "println",
        '"Their product is: "', "print", "*", "println"
    ]).run()

    print("\n** Program 3: Shows branching and looping (use CTRL+D to exit).")
    Machine([
        '"Enter a number: "', "print", "read", "cast_int",
        '"The number "', "print", "dup", "print", '" is "', "print",
        2, "%", 0, "==", '"even."', '"odd."', "if", "println",
        0, "jmp" # loop forever!
    ]).run()


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "repl":
                repl()
            elif cmd == "test":
                test()
                examples()
            else:
                print("Commands: repl, test")
        else:
            repl()
    except EOFError:
        print("")
