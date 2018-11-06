from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import os
import yaml

app = Flask(__name__)
Bootstrap(app)

# Create Database Connection
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
my_sql = MySQL(app)

app.config['SECRET_KEY'] = 'os.urandom(24)'

@app.route('/')
def index():
    blog_posts = None
    cursor = my_sql.connection.cursor()
    result_set = cursor.execute('select * from blog_content order by ts desc')
    if result_set > 0:
        blog_posts = cursor.fetchall()
    if 'login_message' in session.keys():
        message = session['login_message']
        flash(message, category='success')

    return render_template('index.html', blog_posts=blog_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = my_sql.connection.cursor()
        error = None
        cursor.execute("""SELECT * FROM user_info WHERE username = %s""",
            (username,))
        db_user = cursor.fetchone()
        if db_user is None:
            error = 'The user does not exist.'
        elif not check_password_hash(db_user['password'], password):
            error = 'Incorrect password.'
        else:
            session.clear()
            session['username'] = db_user['username']
            session['login_message'] = "Logged in as %s" % (session['username'])
            return redirect(url_for('index'))

        flash(error, category='danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor = my_sql.connection.cursor()
        error = None
        cursor.execute("""SELECT * FROM user_info WHERE username = %s""",
            (username,))
        db_user = cursor.fetchone()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db_user is not None:
            error = 'User {} is already registered.'.format(username)
        elif not (password == confirm_password):
            error = 'Password does not match.'

        if error is None:
            cursor.execute(
                'INSERT INTO user_info (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            my_sql.connection.commit()
            session.clear()
            session['username'] = username
            session['login_message'] = "Logged in as %s" % (session['username'])
            return redirect(url_for('index'))

        flash(error, category='danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'login_message' not in session.keys():
        return redirect(url_for('login'))

    error = None
    if request.method == 'POST':
        title = request.form['title']
        blog_post = request.form['blog_post']
        if not title:
            error = 'Title required.'
        elif not blog_post:
            error = 'Blog post required.'

        if error is None:
            cursor = my_sql.connection.cursor()
            cursor.execute("""
            insert into blog_content (username, title, text) values
            (%s, %s, %s)""", (session['username'], title, blog_post))
            my_sql.connection.commit()
            session['post_message'] = 'Post Successful!'
            return redirect(url_for('post'))

        flash(error, category='warning')

    return render_template('post.html')

@app.route('/edit-post/<int:blog_id>', methods=['GET', 'POST'])
def edit_post(blog_id):
    error = None
    if request.method == 'POST':
        title = request.form['title']
        blog_post = request.form['blog_post']
        if not title:
            error = 'Title required.'
        elif not blog_post:
            error = 'Blog post required.'

        if error is None:
            cursor = my_sql.connection.cursor()
            cursor.execute("""
            update blog_content set
            title = %s,
            text = %s,
            ts = current_timestamp
            where
            blog_id = %s
            """, (title, blog_post, blog_id))
            my_sql.connection.commit()
            session['post_message'] = 'Post Successful!'
            return redirect(url_for('index'))

        flash(error, category='warning')

    cursor = my_sql.connection.cursor()
    cursor.execute("""
    select * from blog_content where blog_id = %s""", (blog_id,))
    db_post = cursor.fetchone()
    return render_template('edit-post.html', db_post=db_post)

@app.route('/delete-post/<int:blog_id>')
def delete_post(blog_id):
    cursor = my_sql.connection.cursor()
    cursor.execute("""
    delete from blog_content where blog_id = %s
    """, (blog_id,))
    my_sql.connection.commit()

    flash('The post has been deleted.', category='success')
    return render_template('delete-post.html')


if __name__ == '__main__':
    app.run(debug=True)
