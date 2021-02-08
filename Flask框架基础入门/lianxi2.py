from flask import Flask, request, session, redirect, render_template, flash, url_for


app = Flask(__name__)


app.secret_key = "asdsadasdasdasd"


@app.route("/")
def index():
    msg = request.args.get("msg")
    if not msg:
        msg = "world"
    return render_template("index.html", msg=msg)


@app.route("/login", methods=['get','post'])
def login():

    msg = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username ,password) == ("shiyanlou", "shiyanlou"):
            session["username"] = username
            flash("you were logged in")
            msg = "shiyanlou"
        else:
            flash("username or password invalid")
        return redirect(url_for("index", msg=msg))

    return render_template("login.html")