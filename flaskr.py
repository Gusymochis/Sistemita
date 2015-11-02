import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_houses():
    cur = g.db.execute('select id, nombre, direccion, vendedor, construccion, terreno, valor, balance, status from casa order by id asc')
    casas = [dict(id=row[0], nombre=row[1], direccion=row[2], vendedor=row[3], construccion=row[4], terreno=row[5], valor=row[6],
             balance=row[7], status=row[8]) for row in cur.fetchall()]
    return render_template('pages/show_houses.html', casas=casas)

@app.route('/getSeller')
def show_sellers():
    cur = g.db.execute('select nombre, apellidos, telefono, email, balance from vendedor order by id desc')
    vendedores = [dict(nombre=row[0], apellidos=row[1], telefono=row[2], email=row[3], balance=row[4]) for row in cur.fetchall()]
    return render_template('pages/show_sellers.html', vendedores=vendedores)

@app.route('/addHouse', methods=['GET', 'POST'])
def add_house():
    error = None
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        g.db.execute('insert into casa (nombre, direccion, vendedor, construccion, terreno, valor, balance, status) values (?, ?, ?, ?, ?, ?, ? ,?)', 
            [request.form['nombre'],request.form['direccion'],request.form['vendedor'],request.form['construccion'],request.form['terreno'],
             request.form['valor'],request.form['balance'],request.form['status']])
        g.db.commit()
        flash('La casa fue agregada satisfactoriamente')
    else:
        cur = g.db.execute('select id, nombre, apellidos from vendedor order by id desc')
        vendedores = [dict(id=row[0], nombre=row[1], apellidos=row[2]) for row in cur.fetchall()]
        return render_template('pages/add_house.html', vendedores=vendedores)
    return render_template('pages/add_house.html', error=error)

@app.route('/addSeller', methods=['GET', 'POST'])
def add_seller():
    error = None
    if not session.get('logged_in'):
        abort(401)
    print request.method
    if request.method == 'POST':
        g.db.execute('insert into vendedor (nombre, apellidos, telefono, email, balance) values (?, ?, ? ,? ,?)',
                     [request.form['nombre'],request.form['apellidos'],request.form['telefono'],request.form['email'],request.form['balance']])        
        g.db.commit()
        flash("Vendedor agregado exitosamente!")
        return redirect(url_for('add_seller'))
    else:
        return render_template('pages/add_seller.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error =  'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('A iniciado Sesion')
            return redirect(url_for('show_houses'))
    return render_template('pages/login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Sesion terminada')
    return redirect(url_for('show_houses'))

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

if __name__ == '__main__':
	app.run()
