from draw_call_stack import outer

cheese = outer()

def end(x):
    cheese()
    print('end'+x)


def subroutine2():
    end('1')
    print('subroutine2')
    end('2')
    end('3')


def subroutine1():
    end('1')
    print('subroutine1')
    subroutine2()


def main():
    print('main')
    subroutine1()

main()