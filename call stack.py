import sys


def cheese():
    stack = []
    frame = sys._getframe().f_back
    while frame:
        stack.append(frame)
        frame = frame.f_back
    stack.reverse()
    print(list(item.f_code.co_name for item in stack))

def step1():
    cheese()

def step2():
    step1()

step2()
