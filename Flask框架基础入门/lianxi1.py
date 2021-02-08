from flask import Flask, render_template


app = Flask(__name__)


@app.route('/<xxx>/')
def get_name(xxx):
    return "{}".format(xxx)


@app.route('/sum/<int:a>/<int:b>')
def sum(a, b):
    return "{}".format(a+b)


@app.route('/')
def index():
    return render_template('index.html')