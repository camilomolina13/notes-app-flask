from flask import Flask, request


from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from notes.routes import notes_bp
from users.routes import users_bp

#db.init_app(app)

# Crear las tablas en la base de datos automáticamente
#with app.app_context():
    #db.create_all()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    app.register_blueprint(notes_bp)
    app.register_blueprint(users_bp)

    @app.route("/acerca-de")
    def about():
        return "Esto es una app de notas"

    @app.route("/contacto", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            return "Formulario enviado correctamente", 201
        return "Pagina de contacto"

    return app

# if __name__ == "__main__":
#     app.run(debug=True)
