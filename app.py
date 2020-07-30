from flask import Flask,render_template,request,redirect,session
import sqlite3
app = Flask(__name__)
app.secret_key ="sunabako"

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
    if "user_id"in session:
        return render_template('add.html')
    else:
        return redirect('/login')

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
    if "user_id"in session:
        

        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute("SELECT id, task FROM task")
        task_list_py =[]
        for row in c.fetchall():
            task_list_py.append({"id":row[0],"task":row[1]})
        c.close()
        print(task_list_py)
        return render_template("tasklist.html",task_list = task_list_py)

    else:
        return redirect('/login')

@app.route("/edit/<int:id>")
def edit(id):
        
    if "user_id"in session:
        
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
        

    else:
        return redirect('/login')

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

@app.route("/del/<int:id>")
def delete(id):
    if "user_id"in session:
        
        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute("DELETE FROM task WHERE id = ?",(id,))
        conn.commit()
        c.close()
        return redirect('/list')

    else:
        return redirect('/login')
@app.route('/regist')
def regist_get():
    if "user_id" in session:
        return redirect('/list')
    else:
        return render_template('regist.html')
    
    

@app.route('/regist',methods=["POST"])
def regist_post():
    py_name = request.form.get("member_name")
    py_password = request.form.get("member_password")
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("INSERT INTO member VALUES (null,?,?)",(py_name,py_password))
    conn.commit()
    c.close()
    return redirect('/login')

@app.route('/login')
def login_get():
    if "user_id" in session:
        return redirect('/list')
    else:
        return render_template('login.html')

@app.route('/login',methods=["POST"])
def login_post():
    py_name = request.form.get('member_name')
    py_password = request.form.get('member_password')
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("SELECT id FROM member WHERE name =? AND password = ?",(py_name,py_password))
    user_id =c.fetchone()
    c.close()
    if user_id is None:
        return render_template('/login.html')
    else:
        session["user_id"] = user_id
        return redirect("/list")

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect("/login")

@app.errorhandler(404)
def notfound(code):
    return "404エラーだお_:(´ཀ`」 ∠):"





if __name__ == '__main__':
    app.run(debug=True)
    

