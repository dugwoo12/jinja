from flask import Flask,jsonify,g,request, render_template, session, redirect, escape, url_for
import sqlite3
DATABASE='./db/test.db'
app=Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv= cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
    db.commit()

def add_student(id,password,email):
    sql = "INSERT INTO join1 (id, password, email) VALUES('%s', '%s', '%s')" %(id,password,email)
    print sql
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res
  
def find_student (name=''):
    sql = "select * from students where name = '%s' limit 1"%(name)
    print sql
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res[0]
def find_student1(name):
    sql = "select * from '%s'"%(name)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res


@app.route('/add', methods = ['GET','POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add1.html')
    else:
        add_student(id=request.form['id'], password=request.form['password'],email=request.form['email'])
    return ''
@app.route('/add1',methods=['GET','POST'])
def add_user1():
    if request.method == 'GET':
        data=request.args.get('table')
        data1=find_student1(data)
        return render_template('add.html',body_data=data1)
    else:
        data=[]
        data=find_student1()
        return render_template('add.html',body_data=data)
    

@app.route('/find_user')
def find_user_by_name():
    name=request.args.get('name','')
    student=find_student(name)
    return jsonify(name=student['name'],age=student['age'],sex=student['sex'])
def find_username():
    sql = "select * from join1 where id = '%s'"%(id)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res

@app.route('/')
def index():
    if 'id' in session:
        return 'Logged in as %s' % escape(session['id'])
    return 'You are not logged in'
#@app.route('/login', method =='POST'):
#def login():
#    if request.method =='POST':
#        session['username'] = request.form['username']
#        return redirect(url_for('index'))
    

    


if __name__=='__main__':
 
    app.run(debug=True, host='0.0.0.0', port=8086)

