from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/dhan/adb/myflaskapp/blog.db'
db=SQLAlchemy (app)
class users(db.Model):
    name =db.Column(db.String(50),primary_key=True)
    email=db.Column(db.String(100))
    username=db.Column(db.String(100))
    password=db.Column(db.String(100))

class articles(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String(200))
    body=db.Column(db.String(4000))
    author=db.Column(db.String(100))

#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('index.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
def articles1():
    # Create cursor
    #cur = db.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")

    #articles = cur.fetchall()
    article_list=articles.query.all()
    if article_list is not None:
        return render_template('articles.html', articles=article_list)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    #cur.close()


#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    #cur = db.connection.cursor()

    # Get article
    #result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = articles.query.filter_by(id=id).first()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        new_user=users(name=name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        # Create cursor
        #cur = db.connection.cursor()

        # Execute query
        #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        #db.connection.commit()

        # Close connection
        #cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        #cur = db.connection.cursor()

        # Get user by username
        #result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        result=users.query.filter_by(username=username).one()
        import pdb; #pdb.set_trace()
        if result is not None:
            # Get stored hash
            #data = cur.fetchone()
            #password = data['password']
            password=result.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    #cur = db.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    article_list=articles.query.filter_by(author=session['username']).all()

    #articles = cur.fetchall()

    if article_list is not None:
        return render_template('dashboard.html', articles=article_list)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    #cur.close()

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        #cur = db.connection.cursor()

        # Execute
        new_article=articles(title=title, body=body, author=session['username'])
        db.session.add(new_article)
        db.session.commit()
        #cur.execute("INSERT INTO articles1(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        #db.connection.commit()

        #Close connection
        #cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    article = articles.query.filter_by(id=id).first()
    # Create cursor
    #cur = db.connection.cursor()

    # Get article by id
    #result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    #article = cur.fetchone()
    #cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        article.title=title
        article.body=body
        # Create Cursor
        #cur = db.connection.cursor()
        app.logger.info(title)
        db.session.commit()
        # Execute
        #cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        #db.connection.commit()

        #Close connection
        #cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = db.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    db.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
