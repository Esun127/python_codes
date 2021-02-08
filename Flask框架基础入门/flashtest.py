from flask import Flask, flash, render_template, url_for, flash, request,redirect



app = Flask(__name__)


# 设置安全密钥
app.secret_key = 'asdasdasdasdase'


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=['get','post'])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "123456":
            error = "Invalid credentials"
            app.logger.error(error)
        else:
            flash("You were successfully logged in") # 记录闪现
            return redirect(url_for("index"))
    return render_template("login.html", error=error)