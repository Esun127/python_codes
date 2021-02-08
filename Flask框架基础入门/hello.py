from flask import Flask, render_template, redirect, abort, url_for, make_response


app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    # return "Hello World!"
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    return "User {}".format(username)
    

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post {}".format(post_id)


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return "Subpath {}".format(subpath)

@app.route('/money/<float:yuan>')
def how_much(yuan):
    return "Money {}".format(yuan)


@app.route('/projects/')
def projects():
    return "The project page"

@app.route('/about')
def about():
    return 'The about page'


@app.errorhandler(401)
def page_not_found(error):
    resp = make_response(render_template("401.html"), 404)
    resp.headers["X-Something"] = "A value"
    # return render_template('401.html') , 404
    return resp   