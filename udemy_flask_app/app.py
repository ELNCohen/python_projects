from flask import Flask, render_template, request, session, flash
from flask_bootstrap import Bootstrap
import yaml
from flask_mysqldb import MySQL
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)

# Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
my_sql = MySQL(app)

app.config['SECRET_KEY'] = 'os.urandom(24)'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name, age = form['name'], form['age']
            name = generate_password_hash(name)
            cur = my_sql.connection.cursor()
            cur.execute("""insert into employee (name, age) values (%s, %s)""", (name, age))
            my_sql.connection.commit()
            flash(message='Successfully inserted data', category='success')
        except:
            flash(message='Insert not successful', category='danger')
    return render_template('index.html')

@app.route('/employees')
def employees():
    cur = my_sql.connection.cursor()
    result = cur.execute("""select * from employee""")
    if result > 0:
        employees = cur.fetchall()
        # return str(check_password_hash(employees[2]['name'], 'short'))
        return render_template('employees.html', employees=employees)
