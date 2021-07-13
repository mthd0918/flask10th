
from sqlite3.dbapi2 import connect
from flask import Flask,render_template,request,redirect,session
import sqlite3
import random


from flask.wrappers import Request
from werkzeug.utils import redirect
app = Flask(__name__)
app.secret_key="jsltqn4398quwyi-0i["

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
    return redirect('/list')

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


@app.route('/edit_get/<task_id>')
def edit_get(task_id):
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBから値をtaskテーブルから取得
    c.execute('select name from task where id = ?', (task_id))
    #タプル型から値を取り出す、('')を取り除く
    py_task = c.fetchone()[0]
    c.close()
    return render_template('edit.html', html_id=task_id, html_task =py_task)

@app.route('/edit_post', methods=['POST'])
def edit_post():
    #htmlの入力フォームから受け取る
    py_id = request.form.get('html_id')
    py_name = request.form.get('html_task')
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBに値を挿入するSQL
    c.execute('UPDATE task SET name = ? WHERE id = ?',(py_name, py_id))
    #DBに変更を加え保存
    conn.commit()
    c.close()
    return redirect('/list')

@app.route('/delete/<task_id>')
def delete(task_id):
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBから値を削除する
    c.execute('delete from task WHERE id = ?',(task_id,))
    #DBに変更を加え保存
    conn.commit()
    c.close()
    return redirect('/list')

@app.route('/regist_get')
def regist_get():
    return render_template('regist.html')

#flask25
@app.route('/regist_post', methods=['POST'])
def regist_post():
    py_name = request.form.get('html_name')
    py_pass = request.form.get('html_pswd')
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBに値を挿入するSQL
    c.execute('insert into account values(null, ?, ?)',(py_name, py_pass))
    #DBに変更を加え保存
    conn.commit()
    c.close()
    return render_template('login.html')

@app.route('/login_get')
def login_get():
    return render_template('login.html')

@app.route('/login_post', methods=['POST'])    
def login_post():
    py_name = request.form.get('html_name')
    py_pass = request.form.get('html_pswd')
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    #DBから値をaccountテーブルから取得
    c.execute('select id from account where name = ? and password = ?', (py_name, py_pass))
    py_id = c.fetchone()
    c.close()
    #idが空っぽだった場合はログイン画面、そうじゃなければリスト画面
    if py_id is None:
        return render_template('/login.html')
    else:
        #クッキーとして、ブラウザにログイン情報を保存
        session['user_id'] = py_id[0]
        return redirect('/list')



@app.errorhandler(404)
def not_found(error):
    return 'お探しのページは見つかりませんでした'

## おまじない
if __name__ == "__main__":
    app.run(debug=True)