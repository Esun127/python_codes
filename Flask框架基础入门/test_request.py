from flask import Flask, request
from flask import environ


app = Flask(__name__)


@app.route('/hello', methods=['POST'])
def hello():
    return "hello"


def test1():
    with app.test_request_context('/hello', method='POST'):
        print( request.path == '/hello')
        print( request.method == 'POST')

def test2():
    with app.request_context(environ):
        print(request.method == 'POST')



if __name__ == "__main__":
    test1()
    test2()