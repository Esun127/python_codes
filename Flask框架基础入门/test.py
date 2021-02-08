from flask import Flask, escape, session, request, render_template, redirect, url_for


app = Flask(__name__)

# 使用会话, 必须设置密钥
app.secret_key = "adasdw2eqweqwe"


@app.route("/")
def index():
    if "username" in session:
        return "Logged in as {}".format(escape(session['username']))
    return "You are not logged in"


@app.route("/login", methods=['get','post'])
def login():
    if request.method == "POST":
        session['username'] = request.form["username"]
        return redirect(url_for("index"))
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("index"))
