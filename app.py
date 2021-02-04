import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash
from FDataBase import FDataBase
import time

# Конфиг БД
DATABASE = '/tmp/reviews.bd'
DEBUG = True
SECRET_KEY = 'fklwefn^#$mflegnr@?23'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'reviews.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# Главная
@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


# Отзывы
@app.route("/reviews", methods=["POST", "GET"])
def rute():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('rev.html', rev=dbase.getRev())


# Создание отзывов
@app.route("/create-rev", methods=["POST", "GET"])
def create_rev():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['revi']) > 10:
            res = dbase.addRev(request.form['name'], request.form['revi'], request.form['carbrand'] )
            if not res:
                print('Ошибка добавления отзыва')
            else:
                print('Отзыв успешно добавлен')
        else:
            print('Ошибка добавления статьи')
    return render_template('create_rev.html')


# Блог
@app.route("/blog", methods=["POST", "GET"])
def blog():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('blog.html', post=dbase.getPostAnonce())


# Услуги
@app.route("/services", methods=["POST", "GET"])
def price():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('services.html', post=dbase.getServAnonce())


# Отображение услуг для Отдельных страниц
@app.route("/full-service/<alias>")
def showServices(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getServ(alias)
    return render_template('full-service.html', title=title, post=post)


# Отображение постов из блога
@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    return render_template('post.html', title=title, post=post)


# Создание постов для блога
@app.route("/create_post", methods=['POST', 'GET'])
def create_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['title']) > 4 and len(request.form['text']) > 10:
            res = dbase.addPost(request.form['title'], request.form['text'], request.form['url'])
            if not res:
                print('Ошибка добавления отзыва')
            else:
                print('Отзыв успешно добавлен')
        else:
            print('Ошибка добавления статьи')
    return render_template('create_post.html')


# Юзер логин
@app.route("/u_log")
def login():
    return render_template('login.html')


# Тесты
@app.route("/test", methods=["POST", "GET"])
def test():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('test.html', test=dbase.getTests())


# Страница 404
@app.errorhandler(404)
def pageNot(error):
    return ("Cтраница не найдена", 404)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

if __name__ == "__main__":
    app.run(debug=True)