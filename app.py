from flask import Flask,render_template
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
    name="hidechika"
    age="25"
    address="那覇市国場1184-6"
    return render_template("dbtest.html", html_name=name , html_age=age , html_address=address)



## おまじない
if __name__ == "__main__":
    app.run(debug=True)