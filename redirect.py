import sys


class Input:
    def __init__(self, text:str):
        self.text = text

    def readline(self):
        offset = self.text.find('\n')
        if offset == -1:
            res, self.text = self.text[:], ''
        else:
            res, self.text = self.text[:offset], self.text[offset+1:]
        return res


sys.stdin = Input('abc\ndef\nhij')

s=''
while True:
    try:
        s += input()
    except EOFError:
        break

print(s)



