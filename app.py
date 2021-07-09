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
    today_whether = '晴れ'
    return render_template('whether.html', today_wheather=wheather)


## おまじない
if __name__ == "__main__":
    app.run(debug=True)