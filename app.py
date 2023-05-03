import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, redirect, session, abort, g

# конфигурация
DATABASE = '/tmp/sauna.db'
DEBUG = True
SECRET_KEY = 'fawheoilnfweaughsaweogihanfk'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fawheoilnfweaughsaweogihanfk'
app.config.from_object(__name__) #из модуля загружается "Конфигурация"

#переопределение пути к базе данных
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'sauna.db')))

#Общая функция для соеденеия с базой данных
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

#Создает базу данных с набором таблиц
def create_db():
    '''Вспомогательная функция для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode = 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/index')
@app.route('/')
def index():
    db = get_db()
    return render_template('index.html')

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

#Это ветка log-in

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    
    if request.method =='POST':
        #print(request.form)
        
        #Нужно добавить ещё критерии
        
        if len(request.form['username']) >= 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        
    
    return render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method =='POST' and request.form['username'] == 'admin' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html')


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != 'username':
        abort(401)
    
    return f'Профиль {username}'

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/discount')
def discount():
    return render_template('discount.html')


@app.route('/service')
def service():
    return render_template('service.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html')


if __name__ == "__main__":
    app.run(debug=True)
