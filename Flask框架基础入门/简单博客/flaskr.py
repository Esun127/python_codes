import sqlite3;
from flask import Flask, render_template, g, flash, request, session, abort, redirect, url_for


# 配置项目
DATABASE = "/tmp/flaskr.db"
ENV = "development"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "123456"

# 创建应用
app = Flask(__name__)

# app.config.from_object() 用于获取对象的属性用以增加配置项
app.config.from_object(__name__) # 从本身(文件)读取配置项

# app.config.from_envvar() 用于从环境变量中加载配置项
app.config.from_envvar("FLASKR_SETTINGS", silent=True)


# 获取数据库连接对象
def db_conn():
    """创建与数据库连接的对象"""
    return sqlite3.connect(app.config["DATABASE"])



# 数据库代码初始化
def init_db():
    """此函数用于创建数据表, 需要在flask shell里面运行"""
    with db_conn() as conn: # 获取数据库的连接引用
        with app.open_resource("schema.sql") as f: #获取文件schema.sql的对象引用
            conn.cursor().executescript(f.read().decode()) # 获取游标对象,并执行多SQL二进制文本内容
        conn.commit()



# @app.before_request 功能: 当任意视图函数执行时, 预先执行这个装饰器下的所有函数
@app.before_request
def before():
    """创建数据库的连接对象, 并将其赋值给g的conn属性"""
    # Flask应用中有两种上下文对象: 应用上下文对象, 请求上下文对象
    # g 是一个应用上下文对象, 它的生存周期却是一次请求的收发
    # 也就是说, 应用每收到一次请求就会产生一个g对象
    # 在生存周期内, 它可以在任意视图函数中被使用
    g.conn = db_conn()


# @app.after_request 功能: 在任意视图函数执行完毕之后执行, 除非视图函数执行时遇到异常
# @app.teardown_request 与app.after_request 作用一样, 但是它可以无视视图函数触发的任何异常, 保证一定被执行, 其中的参数为可能出现的异常

@app.teardown_request
def teardown(exception):
    """关闭与数据库的连接"""
    g.conn.close()


@app.route("/")
def show_entries():
    """显示所有存储在数据表中的条目"""
    cursor = g.conn.cursor()
    cursor.execute("SELECT title, text FROM entries ORDER BY id DESC")
    # 查询结果集
    entries = [dict(title=row[0], text=row[1]) for row in  cursor.fetchall()]
    return render_template("show_entries.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    """ 添加一篇博客"""
    if not session.get("login"):
        abort(401)

    g.conn.cursor().execute("INSERT INTO entries (title, text) VALUES (?, ?)", [request.form.get("title"), request.form.get("text")])
    g.conn.commit()
    flash("New entry has been succcessfully posted")
    return redirect(url_for("show_entries"))


@app.route("/login", methods=["GET","POST"])
def login():
    """用户登录"""
    error = None
    if request.method == "POST":
        if request.form.get("username") != app.config.get("USERNAME"):
            error = error + " Invalid username" if error else "Invalid username"
        if request.form.get("password") != app.config.get("PASSWORD"):
            error = error + " Invalid password" if error else "Invalid password"
        if error is None:
            session['login']  = True
            flash("You are logginned successfully!")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """登出"""
    session.pop("login", None)
    flash("You have logouted successfully")
    return redirect(url_for("show_entries"))





if __name__ == "__main__":
    app.run()