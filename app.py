from flask import Flask,render_template,request,redirect
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

@app.route('/add',methods=['post'])
def app_post():
    py_task = request.form.get("task")
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("INSERT INTO task VALUES (null,?)",(py_task,))
    conn.commit()
    conn.close()
    return redirect('/list')

@app.route('/list')
def task_list():
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM task")
    task_list_py =[]
    for row in c.fetchall():
        task_list_py.append({"id":row[0],"task":row[1]})
    c.close()
    print(task_list_py)
    return render_template("tasklist.html",task_list = task_list_py)


@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("SELECT task FROM task WHERE id =?",(id,))
    py_task=c.fetchone()
    print(py_task)
    c.close()
    if py_task is None:
        return "タスクがありません(๑╹ω╹๑ )"
    else:
        task = py_task[0]
        py_item={"dic_id":id,"dic_task":task}
        return render_template("edit.html",html_task = py_item)

@app.route("/edit",methods=['post'])
def update_task():
    item_id = request.form.get("task_id")
    #入力フォームから撮ってきた時点では文字列なのでint型に変換
    item_id = int(item_id)
    py_task = request.form.get('task')
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("UPDATE task SET task = ? WHERE id = ?",(py_task,item_id))
    conn.commit()
    c.close()
    return redirect('/list')

@app.errorhandler(404)
def notfound(code):
    return "404エラーだお_:(´ཀ`」 ∠):"





if __name__ == '__main__':
    app.run(debug=True)
    

