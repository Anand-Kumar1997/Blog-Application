import datetime
from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine(
    'mssql+pyodbc://RS-PC\\SQLEXPRESS/BlogDb?driver=SQL+Server+Native+Client+11.0', convert_unicode=True)
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.Users
Blog = Base.classes.Blogs

# print(User)
# print(Blog)

# If you have default fernet key
f_key = 'wrbcK7TU_S8mPA-YYO5ZoqIh90huixAHE_oI0n33cKw='.encode()
f = Fernet(f_key)


# Run following code when need a new key
# key = Fernet.generate_key()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ksjdbsd ksdjbfksjdfksjdbfk;jsdhfksjdfklj'


@app.route('/')
def index():
    ssn = Session(engine)
    data = ssn.query(Blog).all()
    data1 = ssn.query(User).all()

    blog_list = []
    for i in data:
        d = {'Title': i.Title, 'Writeup': '{}'.format(i.Writeup[:200]), 'CreateDT': i.CreateDT.strftime("%A, %B %d, %Y - %I:%m %p"), 'BlogId': i.BlogId}
        for j in data1:
            if i.UserEmail == j.Email:
                d['Owner'] = j.Name

        blog_list.append(d)
    ssn.close()
    return render_template('index.html', blog_list=blog_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in', None):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['txtEmail']
        psw = request.form['txtPwd']
        # enc_pwd = f.encrypt(psw.encode())

        ssn = Session(engine)

        data = ssn.query(User).filter_by(Email=email).first()
        if data:

            if email == data.Email and (psw == f.decrypt(data.Password.encode()).decode()):
                status = True
                session['logged_in'] = True
                session['UserName'] = data.Name
                session['UserEmail'] = data.Email
            else:
                status = False
            ssn.close()
        else:
            status = False

        if not status:
            return render_template('login.html', msg='Login failed.')
        else:
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in', None):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['txtName']
        email = request.form['txtEmail']
        pwd = request.form['txtPwd']
        dt = datetime.datetime.now()
        # print(email, name, pwd, dt)

        enc_pwd = f.encrypt(pwd.encode())
        new_user = User(Email=email, Name=name,
                        Password=enc_pwd.decode(), JoiningDT=dt)

        ssn = Session(engine)
        try:
            ssn.add(new_user)
            ssn.commit()
            status = True
        except:
            status = False
        finally:
            ssn.close()

        msg = 'You are registered successfully.' if status else 'Registration failed.'

        return render_template('register.html', status=status, msg=msg)
    else:
        return render_template('register.html')


@app.route('/social')
def social():
    ssn = Session(engine)
    user_list = ssn.query(User).all()
    users = []
    for user in user_list:
        u = {'name': user.Name, 'email': user.Email}
        users.append(u)
    ssn.close()

    return render_template('social.html', users=users)


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in', None):
        return render_template('dashboard.html', name=session['UserName'])
    else:
        return redirect(url_for('login'))


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    msg = None
    if session.get('logged_in', None):

        if request.method == 'POST':
            userEmail = session['UserEmail']
            title = request.form['title']
            writeup = request.form['writeup']
            createDT = datetime.datetime.now()

            blog_user = Blog(UserEmail=userEmail, Title=title,
                             Writeup=writeup, CreateDT=createDT)
            ssn = Session(engine)
            try:
                ssn.add(blog_user)
                ssn.commit()
                status = True
            except:
                status = False
            finally:
                ssn.close()

            msg = 'Your Blog is succesfully Added.' if status else 'Added failed.'
        return render_template('add_blog.html', name=session['UserName'], msg=msg, status=status)

    else:
        return render_template('add_blog.html')


@app.route('/my_blog')
def my_blog():

    ssn = Session(engine)
    blog_list = ssn.query(Blog).filter_by(UserEmail=session['UserEmail']).all()
    blogs = []
    for blog in blog_list:
        u = {'title': blog.Title, 'writeup': blog.Writeup,
             'dt': blog.CreateDT.strftime("%A, %B %d, %Y - %I:%m %p")}
        blogs.append(u)
    ssn.close()

    return render_template('my_blog.html', blogs=blogs)


@app.route('/full_blog_content/<int:BlogID>')
def full_blog_content(BlogID):
    ssn = Session(engine)
    blog_list = ssn.query(Blog).filter_by(BlogId=BlogID).all()
    user_list = ssn.query(User).all()
    full_blog_list = []
    msg = None
    if blog_list:
        for i in blog_list:
            d = {'Title': i.Title, 'Writeup': i.Writeup,
                 'CreateDT': i.CreateDT.strftime("%A, %B %d, %Y - %I:%m %p")}
            for j in user_list:
                if i.UserEmail == j.Email:
                    d['Owner'] = j.Name
            status = True
            full_blog_list.append(d)
        ssn.close()

    else:
        status = False
        msg = 'Content Not Found!'
        ssn.close()
    return render_template('full_blog_content.html', msg=msg, status=status, full_blog=full_blog_list)


if __name__ == "__main__":
    app.run(debug=True)
