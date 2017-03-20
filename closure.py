def outer():
    A = 3
    B = 4
    def inner():
        return A+1
    inner.author = 'Guo'
    return inner

f = outer()
