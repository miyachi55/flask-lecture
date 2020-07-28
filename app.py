from flask import Flask,render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello():
    return"Hello World!"

@app.route('/top')
def top():
    return"なにもっと見てんだよ( ^ω^ )"

@app.route('/hello/<text>')
def name(text):
    return text +"さん、こんにちは( ´∀｀)"

@app.route('/index')
def index():
    name="Zxys"
    age = 25
    adress ="高松市"
    return render_template('index.html',user_name = name,user_adress = adress,user_age = age)

@app.route('/weather')
def weather():
    ten="晴れ"
    return render_template('weather.html',today =ten)

@app.route('/dbtest')
def dbtest():
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()

    c.execute("SELECT name,age,addres FROM user WHERE id = 1")
    user_info = c.fetchone()
    
    c.close()

    print(user_info)

    return render_template('dbtest.html',db_userinfo = user_info)

@app.route('/add')
def add_get():
    return render_template('add.html')
    



if __name__ == '__main__':
    app.run(debug=True)
    

