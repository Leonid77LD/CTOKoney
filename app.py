import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash, redirect
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from UserLogin import UserLogin

# Конфиг БД
DATABASE = '/tmp/reviews.bd'
DEBUG = True
SECRET_KEY = 'fklwefn^#$mflegnr@?23'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'reviews.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


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

dbase = None
@app.before_request
def before_reqest():
    "Установка соединения с БД перед выполненем запроса"
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# Главная
@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


# Отзывы
@app.route("/reviews", methods=["POST", "GET"])
def rute():
    return render_template('rev.html', rev=dbase.getRev())


# Создание отзывов
@app.route("/create-rev", methods=["POST", "GET"])
def create_rev():
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


# Эвакуатор
@app.route("/tow")
def tow():
    return render_template('tow.html')


# Запчасти
@app.route("/spares")
def spares():
    return render_template('spares.html')


# Контакты
@app.route("/contacts")
def contacts():
    return render_template('contacts.html')


# Блог
@app.route("/blog", methods=["POST", "GET"])
def blog():
    return render_template('blog.html', post=dbase.getPostAnonce())


# Услуги
@app.route("/services", methods=["POST", "GET"])
def price():
    return render_template('services.html', post=dbase.getServAnonce())


# Отображение услуг для Отдельных страниц
@app.route("/full-service/<alias>")
def showServices(alias):
    title, post = dbase.getServ(alias)
    return render_template('full-service.html', title=title, post=post)


# Отображение постов из блога
@app.route("/post/<alias>")
def showPost(alias):
    title, post = dbase.getPost(alias)
    return render_template('post.html', title=title, post=post)


# Создание постов для блога
@app.route("/create_post", methods=['POST', 'GET'])
@login_required
def create_post():
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


# Админ логин
@app.route("/u_log", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByName(request.form['name'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('admin_menu'))

    return render_template("login.html")


# Админ меню
@app.route("/Admin_menu")
@login_required
def admin_menu():
    return render_template("admin_menu.html")


# Выход из режима Админа
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Тесты
@app.route("/test", methods=["POST", "GET"])
def test():
    return render_template('test.html', test=dbase.getTests())


# Страница 404
@app.errorhandler(404)
def pageNot(error):
    return render_template('error404.html')


# Закрытие БД
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

if __name__ == "__main__":
    app.run(debug=True)