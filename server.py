#!/usr/bin/env python2.7
import re
import datetime
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, abort, url_for, render_template, g, redirect, Response,session
import json
import datetime

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key='rz2390ps2997project'

DATABASEURI = "postgresql://rz2390:rz2390ps2997project@35.231.44.137/proj1part2"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/register')
def another():
  return render_template("register.html")

@app.route('/login')
def another2():
  return render_template("login.html")

@app.route('/update')
def another3():
  return render_template("update.html")

@app.route('/reviewAdd')
def another4():
  return render_template("reviewAdd.html")

@app.route('/movieDisplay/<movieid>')
def displayMovie(movieid):
  context=movieinfo(movieid)
  return render_template("movieDisplay.html",**context)

@app.route('/reviewDisplay/<reviewid>')
def displayReview(reviewid):
  cursor=g.conn.execute('''SELECT * FROM review WHERE reviewid='''+str(session['reviewid']))
  liked=str(cursor.fetchone()[5]+1)
  cursor.close()
  cursor=g.conn.execute('''UPDATE review SET reviewid=%s,userid=%s,movieid=%s,comment=%s,rating=%s,liked=%s,modifiedtime=%s WHERE reviewid='''+str(session['reviewid']), (str(session['reviewid']),str(session['ruserid']),str(session['rmovieid']),session['comment'],str(session['rating']),liked,session['modifiedtime']))
  cursor.close()
  session['liked']=int(liked)
  context=reviewinfo(reviewid)
  return render_template("reviewDisplay.html",**context)

@app.route('/movieDisplay/reviewDisplay/<reviewid>')
def displayReview2(reviewid):
  cursor=g.conn.execute('''SELECT * FROM review WHERE reviewid='''+str(session['reviewid']))
  liked=str(cursor.fetchone()[5]+1)
  cursor.close()
  cursor=g.conn.execute('''UPDATE review SET reviewid=%s,userid=%s,movieid=%s,comment=%s,rating=%s,liked=%s,modifiedtime=%s WHERE reviewid='''+str(session['reviewid']), (str(session['reviewid']),str(session['ruserid']),str(session['rmovieid']),session['comment'],str(session['rating']),liked,session['modifiedtime']))
  cursor.close()
  session['liked']=int(liked)
  context=reviewinfo(reviewid)
  return render_template("reviewDisplay.html",**context)

@app.route('/reviewAdd', methods=['POST'])
def review():
  comment=request.form['comment']
  rating=request.form['rating']
  try:
    if 'userid' not in session:
      return render_template("login.html")
    userid=session['userid']
    reviewidl=g.conn.execute('''SELECT COUNT(*) FROM review''')
    s=list(reviewidl)
    #s='[(11L,)]'
    n=re.findall('(\d+L,)',str(s))
    if n!=[]:
      nS=re.findall('\d+',n[0])
      reviewid=int(nS[0])+1
    else:
      print("emmm")
    liked=0
    t=str(datetime.datetime.now())
    modifiedtime=t[:10]
    movieid=session['movieid']
    g.conn.execute('''INSERT INTO review (reviewid,userid,movieid,comment,rating,liked,modifiedtime) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (reviewid,userid,movieid,comment,rating,liked,modifiedtime))
    context=profile(userid)
    reviewidl.close()
    return render_template("profile.html", **context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('reviewAdd.html')
  #return redirect(url_for('reviewAdd'))

@app.route('/update', methods=['POST'])
def update():
  print("session:",session)
  print("request.form:",request.form)
  description=request.form['description']
  gender=request.form['gender']
  imageurl=request.form['imageurl']
  password=request.form['password']
  nickname=request.form['nickname']
  age=request.form['age']
  email=request.form['email']
  userid=session['userid']
  if not password:
    password=session['password']
  if not nickname:
    nickname=session['nickname']
  if not age:
    age=session['age']
  if not gender:
    gender=session['gender']
  if not imageurl:
    imageurl=session['imageurl']
  if not email:
    email=session['email']
  if not description:
    description=session['description']
  try:
    cursor=g.conn.execute('''UPDATE users SET userid=%s,password=%s,nickname=%s,age=%s,gender=%s,imageurl=%s,email=%s,description=%s WHERE userid='''+str(userid), (userid,password,nickname,age,gender,imageurl,email,description))
    context=profile(userid)
    cursor.close()
    return render_template("profile.html", **context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('update.html')

@app.route('/login', methods=['POST'])
def login():
  userid=request.form['userid']
  session['userid']=userid
  password=request.form['password']
  try:
    loginf=g.conn.execute('''SELECT userid FROM users WHERE userid = %s AND password = %s''',
                             (userid, password))
    loginff=loginf.fetchone()
    if loginff:
      context=profile(userid)
      s=g.conn.execute('SELECT * FROM users WHERE userid=%s',userid)
      ss=s.fetchone()
      session['userid']=ss[0]
      session['password']=ss[1]
      session['nickname']=ss[2]
      session['age']=ss[3]
      session['gender']=ss[4]
      session['imageurl']=ss[5]
      session['email']=ss[6]
      session['description']=ss[7]
      loginf.close()
      s.close()
      return render_template("profile.html", **context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
  description=request.form['description']
  gender=request.form['gender']
  imageurl=request.form['imageurl']
  password=request.form['password']
  nickname=request.form['nickname']
  age=request.form['age']
  email=request.form['email']
  #print("name:",name)
  try:
    useridl=g.conn.execute('''SELECT COUNT(*) FROM users''')
    s=list(useridl)
    #s='[(11L,)]'
    n=re.findall('(\d+L,)',str(s))
    if n!=[]:
      nS=re.findall('\d+',n[0])
      userid=int(nS[0])+1
    else:
      print("emmm")
    g.conn.execute('''INSERT INTO users (userid,password,nickname,age,gender,imageurl,email,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', (userid,password,nickname,age,gender,imageurl,email,description))
    context=profile(userid)
    useridl.close()
    return render_template("profile.html", **context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('register.html')

def profile(id):
  cursor = g.conn.execute("SELECT * FROM users WHERE userid="+str(id))
  datas = []
  for result in cursor:
    datas.append(result)
  cursor.close()
  cursor2=g.conn.execute("SELECT * FROM review WHERE userid=%s",str(id))
  datas2=[]
  for result in cursor2:
    datas2.append(result)
  cursor2.close()
  datastotal=datas+datas2
  context = dict(data = datastotal)
  return context

def movieinfo(id):
  try:
    cursor=g.conn.execute('''SELECT * FROM movie WHERE movieid = '''+str(id))
    datas = []
    for result in cursor:
      datas.append(result)
    cursor.close()
    cursor=g.conn.execute('''SELECT * FROM movie WHERE movieid = '''+str(id))
    ss=cursor.fetchone()
    session['movieid']=ss[0]
    session['title']=ss[1]
    session['popularity']=ss[2]
    session['genre']=ss[3]
    session['revenue']=ss[4]
    cursor.close()
    cursor=g.conn.execute("SELECT * FROM review WHERE movieid=%s",str(id))
    datas2=[]
    for result in cursor:
      datas2.append(result)
    cursor.close()
    datastotal=datas+datas2
    context = dict(data = datastotal)
    return context
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('index.html')

def reviewinfo(id):
  try:
    cursor=g.conn.execute('''SELECT * FROM review WHERE reviewid = '''+str(id))
    datas = []
    for result in cursor:
      datas.append(result)
    cursor.close()
    cursor=g.conn.execute('''SELECT * FROM review WHERE reviewid = '''+str(id))
    ss=cursor.fetchone()
    session['reviewid']=ss[0]
    session['ruserid']=ss[1]
    session['rmovieid']=ss[2]
    session['comment']=ss[3]
    session['rating']=ss[4]
    session['liked']=ss[5]
    session['modifiedtime']=ss[6]
    cursor.close()
    datastotal=datas
    context = dict(data = datastotal)
    return context
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('index.html')

@app.route('/movieListID', methods=['POST'])
def movie():
  movieid=request.form['movie']
  try:
    context=movieinfo(movieid)
    return render_template("movieListID.html", **context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('index.html')

@app.route('/movieListGenre', methods=['POST'])
def movie2():
  genre=request.form['option']
  try:
    cursor=g.conn.execute('''SELECT * FROM movie WHERE genre=%s''',genre)
    datas=[]
    for result in cursor:
      datas.append(result)
    cursor.close()
    print("datas",datas)
    context=dict(data=datas)
    return render_template("movieListGenre.html",**context)
  except Exception as e:
    error=str(e)
    print(error)
  return render_template('index.html')

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
