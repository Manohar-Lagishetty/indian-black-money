from flask import *  
import sqlite3  
  
app = Flask(__name__)  
app.secret_key = "super secret key"

@app.route("/")  
def index():  
    return render_template("index.html")

@app.route('/signup')
def signup():   
    return render_template('signup.html')

@app.route('/signup_success',methods = ['POST'])
def signup_success():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        with sqlite3.connect('admin.db') as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT into Admin (name, email, password) values (?,?,?)",(name,email,password))
                con.commit()
            except:
                msg = 'Duplicate Email cannot add!'
                return render_template('signup.html', msg=msg)
            else:
                return redirect(url_for('login'))

 
@app.route('/login')  
def login():  
    return render_template("login.html")  
 
@app.route('/login_success',methods = ['POST'])  
def success():  
    if request.method == "POST":  
        email = request.form['email']  
        password = request.form['pass']     
    
    with sqlite3.connect('admin.db') as con:
        try: 
            cur = con.cursor()
            cur.execute("select password from Admin where email=?",(email,))
            pswd = cur.fetchone()
            print(pswd)
            con.commit()
        except:
            msg = "Incorrect Email id or Password!!!"
            return render_template('login.html', msg=msg)
        else:
            if pswd == None:
                msg = "Incorrect Email id or Password!!!"
                return render_template('login.html', msg=msg)
            elif pswd[0] == password: 
                session['email'] = email  
                return redirect(url_for('index'))
            else:  
                msg = "Incorrect Email id or Password!!!"
                return render_template('login.html', msg=msg)  
 
 
@app.route("/add")  
def add():
    if 'email' in session:  
        return render_template("add.html")  
    else:
        return redirect(url_for('login'))
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    # msg = "msg"  
    if request.method == "POST": 
        name = request.form["name"]  
        contact = request.form["contact"]  
        email = request.form["email"]  
        salary = request.form["salary"]
        with sqlite3.connect("corrupstion.db") as con:   
            try:  
                cur = con.cursor()  
                cur.execute("INSERT into emp (name, contact, email, salary) values (?,?,?,?)",(name,contact,email,salary))  
                con.commit()  
                msg = "Corrupstionist successfully Added"  
            except:  
                # con.rollback()  
                msg = "We cannot add the Co"  
            finally:  
                return render_template("add_success.html",msg = msg)  
 
@app.route("/view")  
def view():
    if 'email' in session:  
        con = sqlite3.connect("corrupstion.db")  
        con.row_factory = sqlite3.Row  
        cur = con.cursor()  
        cur.execute("select * from emp")  
        rows = cur.fetchall()  
        return render_template("view.html",rows = rows)  
    else:
        return redirect(url_for('login'))
 
@app.route("/update")  
def update():
    if 'email' in session:
        return render_template("update.html")  
    else:
        return redirect(url_for('login'))

@app.route("/updaterecord",methods = ["POST"])  
def updaterecord():  
    id = request.form["id"]  
    with sqlite3.connect("corrupstion.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("select name, contact, email, salary from emp where id = ?",(id,))  
            name, contact, email, salary = cur.fetchone()
            con.commit()
            # msg = "record successfully fetched"  
        except:  
            msg = f"No Record of Id:{id} " 
            return render_template('update_success.html', msg=msg) 
        else:  
            resp = make_response(render_template("update_record.html", id = id, name = name, contact=contact, email = email, salary = salary))
            resp.set_cookie('id',id)
            return resp

@app.route("/updatesuccess",methods = ["POST"])  
def updatesuccess():   
    if request.method == "POST":  
        id = request.cookies.get("id")
        name = request.form["name"] 
        contact = request.form["contact"] 
        email = request.form["email"]  
        salary = request.form["salary"] 
    with sqlite3.connect("corrupstion.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("update emp set name=?, contact=?, email=?, salary=? where id =?",(name, contact, email, salary, id))
            con.commit()
            msg = "Record Successfully Updated"  
        except:  
            msg = "can't be updated"  
        finally: 
            resp = make_response(render_template("update_success.html",msg = msg)) 
            return resp

@app.route("/delete")  
def delete():  
    if 'email' in session:
        return render_template("delete.html") 
    else:
        return redirect(url_for('login'))
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = str(request.form["id"])  
    with sqlite3.connect("corrupstion.db") as con:            
        con.row_factory = sqlite3.Row  # makes a list with obj
        cur = con.cursor()  
        cur.execute("select id from emp where id=?", (id,))  
        tid = cur.fetchone()
        print(tid)
        try: 
            if tid['id'] == int(id): 
                cur.execute("delete from emp where id = ?",(id,))
                msg = "Record Successfully Deleted" 
                con.commit()
        except:
            msg = f"No Employee with id:{id}"
        finally:
            return render_template("delete_success.html",msg = msg) 

@app.route("/search")  
def search():  
    if 'email' in session:
        return render_template("search.html") 
    else:
        return redirect(url_for('login'))

@app.route("/searchrecord",methods = ["POST"])  
def searchrecord():  
    name = str(request.form["name"])  
    if 'email' in session:  
        
        con = sqlite3.connect("corrupstion.db")  
        con.row_factory = sqlite3.Row  
        cur = con.cursor()  
        cur.execute("select * from emp where name=?", (name,))  
        rows = cur.fetchall()  
        print(rows)
        if rows == []:
            msg = "No Such Employee" 
            return render_template('search.html', msg=msg)
        else:
            return render_template("view.html",rows = rows)  
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email',None)
        return redirect(url_for('index')) 

  
if __name__ == "__main__":  
    app.run(debug = True)  