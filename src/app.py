from flask import Flask, redirect, render_template, request, flash, url_for
from flask_mysqldb import MySQL
from config import config
from forms import registerForm, loginForm, contactForm, editcontactForm
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from models.entities.user import User
from models.modelUser import ModelUSer
app = Flask(__name__)
db = MySQL(app)

loggin_manager_app = LoginManager(app)

@loggin_manager_app.user_loader
def user_loader(id):
    user = ModelUSer.get_by_id(db, id)
    return user


@app.route('/')
def inicio():
    return render_template('auth/inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(None, None, email, password)
        logged_user = ModelUSer.login(db, user)
        if logged_user:
            print(logged_user.password)
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('contactos'))
            else:
                flash('CONTRASEÑA INCORRECTA')
        flash('Usuario no encontrado')

    else: 
        if current_user.is_authenticated:
            return redirect(url_for('contactos'))
        return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(username, email, password)

        cur = db.connection.cursor()
        sql = 'SELECT * FROM usuarios WHERE email = %s'
        cur.execute(sql, (email, ))
        row = cur.fetchone()
        if row:
            flash("Este correo ya existe")
            return redirect(url_for('register'))
        else:
            contra = generate_password_hash(password)
            cur = db.connection.cursor()
            sql = 'INSERT INTO usuarios (username, email, password) VALUES(%s, %s, %s)'
            values = (username, email, contra)
            cur.execute(sql, values)
            db.connection.commit()
            flash('Usuario creado correctamente')
            return redirect(url_for('login'))
    else: 
        return render_template('auth/register.html', form=form)


@app.route('/contactos', methods=['POST','GET'])
def contactos():
    form = contactForm()
    if request.method == 'POST':
        return redirect(url_for('logout'))
    else:
        data = ModelUSer.getContactos(db, current_user.id)
        if data:
            return render_template('contactos.html', data=data, form=form)
        return render_template('contactos.html', form=form)

@app.route('/addcontact', methods=['GET', 'POST'])
def addcontact():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        descripcion = request.form.get('descripcion')

        ModelUSer.addContactos(db, nombre, telefono, descripcion, current_user.id)
        flash('Contacto añadido correctamente')
        return redirect(url_for('contactos'))
    else:
        return redirect(url_for('contactos'))

@app.route('/edit/<string:id>', methods=['GET'])
def edit(id):
    form = editcontactForm()
    if request.method == 'GET':
        cur = db.connection.cursor()
        sql = 'SELECT * FROM contactos WHERE id = %s'
        cur.execute(sql,(id,))
        data = cur.fetchall()
        return render_template('editContacto.html',form=form, data=data)
    
@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    descripcion = request.form.get('descripcion')
    cur = db.connection.cursor()
    sql = 'UPDATE contactos SET nombre =%s, telefono=%s, descripcion =%s WHERE id =%s'
    cur.execute(sql, (nombre, telefono, descripcion, id))
    db.connection.commit()
    return redirect(url_for('contactos'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = db.connection.cursor()
    sql = 'DELETE FROM contactos WHERE id = %s'
    cur.execute(sql, (id,))
    db.connection.commit()
    return redirect(url_for('contactos'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('inicio'))
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)

