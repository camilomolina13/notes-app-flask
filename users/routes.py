from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, db

users_bp = Blueprint('users', __name__)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        # Verificar usuario y contraseña
        if user and user.password == password:

            # Guardar información del usuario en la sesión
            session['user_id'] = user.id
            session['username'] = user.username

            flash(f'Bienvenido, {user.username}!', 'success')

            return redirect(url_for('notes.home'))

        flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verificar si ya existe el correo
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash('El correo ya está registrado.', 'warning')
            return render_template('register.html')

        # Verificar si ya existe el username
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            flash('El nombre de usuario ya está registrado.', 'warning')
            return render_template('register.html')

        # Crear usuario
        new_user = User(
            username=username,
            email=email,
            password=password
        )

        # Guardar usuario
        db.session.add(new_user)
        db.session.commit()

        flash(
            'Usuario registrado correctamente. Ahora puedes iniciar sesión.',
            'success'
        )

        return redirect(url_for('users.login'))

    return render_template('register.html')

@users_bp.route('/logout') 
def logout(): # Eliminar los datos de la sesión 
    session.pop("user", None)
    flash('Has cerrado sesión correctamente.', 'success') 
    return redirect(url_for('users.login'))
