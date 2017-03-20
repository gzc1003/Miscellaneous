from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    from draw_call_stack import outer
    cheese = outer()
    cheese()
    return 'Yet another hello!'

if __name__ == '__main__':
    app.run()
