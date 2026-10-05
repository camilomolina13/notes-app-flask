from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Note, User, db

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/')
def home():

    # Verificar si el usuario inició sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a las notas.', 'warning')
        return redirect(url_for('users.login'))

    notes = Note.query.all()
    users = User.query.all()

    return render_template(
        'home.html',
        notes=notes,
        users=users
    )


@notes_bp.route('/create', methods=['GET', 'POST'])
def createNote():

    # Verificar sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión para crear una nota.', 'warning')
        return redirect(url_for('users.login'))

    if request.method == 'POST':

        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Validar longitud del título
        if len(title) < 10:
            flash('El título es muy corto. Mínimo 10 caracteres.', 'error')
            return render_template('note_form.html')

        # Validar longitud del contenido
        if len(content) < 50:
            flash('El contenido es muy corto. Mínimo 50 caracteres.', 'error')
            return render_template('note_form.html')

        # Crear la nota solamente si las validaciones son correctas
        new_note = Note(
            title=title,
            content=content
        )

        db.session.add(new_note)
        db.session.commit()

        flash('Nota creada correctamente.', 'success')

        return redirect(url_for('notes.home'))

    return render_template('note_form.html')


@notes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):

    # Verificar sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión para editar una nota.', 'warning')
        return redirect(url_for('users.login'))

    note = Note.query.get_or_404(id)

    if request.method == 'POST':

        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Validar longitud del título
        if len(title) < 10:
            flash('El título es muy corto. Mínimo 10 caracteres.', 'error')
            return render_template('edit_note.html', note=note)

        # Validar longitud del contenido
        if len(content) < 50:
            flash('El contenido es muy corto. Mínimo 50 caracteres.', 'error')
            return render_template('edit_note.html', note=note)

        # Actualizar la nota solamente si las validaciones son correctas
        note.title = title
        note.content = content

        db.session.commit()

        flash('Nota actualizada correctamente.', 'success')

        return redirect(url_for('notes.home'))

    return render_template('edit_note.html', note=note)


@notes_bp.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):

    # Verificar sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión para eliminar una nota.', 'warning')
        return redirect(url_for('users.login'))

    note = Note.query.get_or_404(id)

    db.session.delete(note)
    db.session.commit()

    flash('Nota eliminada correctamente.', 'success')

    return redirect(url_for('notes.home'))

