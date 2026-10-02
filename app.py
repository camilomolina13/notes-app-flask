from flask import (
    Flask, 
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db,Note

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Crear las tablas en la base de datos automáticamente
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@app.route("/acerca")
def acerca():
    return "Esta aplicación tiene la funcionalidad para tomar notas"


@app.route("/contacto", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente\n", 201
    return "Pagina de contacto"

@app.route("/testHTML")
def testHTML():
    return "<h1>Hola Mundo</h1>"

@app.route("/crear-nota", methods=["GET", "POST"])
def createNote():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        note_db = Note(title=title, content=content)

        db.session.add(note_db)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("note_form.html")


@app.route("/editar-nota/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        note.title = title
        note.content = content

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit_note.html", note=note)


@app.route("/eliminar-nota/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
