from sqlite3.dbapi2 import connect
from flask import Flask,render_template,request
import sqlite3
import random

from flask.wrappers import Request
app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name

@app.route("/greet/<name>")
def greet(name):
    return name + "さん、こんにちは！！"

@app.route('/tpl')
def tpl():
    name = 'hidechika'
    return render_template('index.html', tpl_name=name)

@app.route('/wheather')
def wheather():
    wheather = '晴れ'
    return render_template('wheather.html', today_wheather=wheather)

@app.route('/dbtest')
def dbtest():
    #flasktest.dbに接続
    conn = sqlite3.connect("flasktest.db")
    #DBを操作できるようにする
    c = conn.cursor()
    #SQLを実行
    c.execute('select name,age,address from user where id = 1')
    #SQLで取得したデータをpythonの変数に格納
    user_info = c.fetchone()
    #DBとの接続を終える
    c.close()
    print(user_info)
    return render_template('dbtest.html', html_name=user_info[0] , html_age=user_info[1] , html_address=user_info[2])

@app.route('/color')
def color():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute('select name from color')
    color = c.fetchall()
    c.close()

    print(color)

    color_choice = random.choice(color)
    return render_template('color.html', html_color=color_choice[0])

@app.route('/add_get')
def add_get():
    return render_template('add.html')

#methodのsを気を付ける！
@app.route('/add_post', methods=['POST'])
def add_post():
#HTMLの入力フォームから受け取る
    py_task = request.form.get("html_task")
    print(py_task)
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBに値を挿入するSQL
    c.execute('insert into task values(null, ?)', (py_task,))
    #DBに変更を加え保存
    conn.commit()
    c.close()
    return render_template('add.html')

@app.route('/list')
def list():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBから値をtaskテーブルから取得
    c.execute('select id, name from task')
    py_task = c.fetchall()
    c.close()
    print(py_task)
    #格納用の変数（リスト型）を用意
    task_list=[]
    #DBから持ってきたデータをすべて追加していく
    for item in py_task:
        #taskリストに追加していく
        task_list.append({'id':item[0], 'name':item[1]})

    return render_template('list.html', html_task=task_list)


@app.route('/edit_get')
def edit_get():
    return render_template('edit.html')


@app.errorhandler(404)
def not_found(error):
    return 'お探しのページは見つかりませんでした'

## おまじない
if __name__ == "__main__":
    app.run(debug=True)