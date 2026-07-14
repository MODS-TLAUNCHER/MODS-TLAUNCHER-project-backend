from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ==========================================
# Conexión PostgreSQL Docker
# ==========================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@127.0.0.1:5432/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# Entidad Usuario
# Representa la tabla usuario
# ==========================================

class Usuario(db.Model):

    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'bienestar'}

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150))
    correo_institucional = db.Column(db.String(150))

# ==========================================
# Endpoint Hola Mundo
# ==========================================

@app.route('/hola')
def hola():

    usuario = Usuario.query.first()

    if usuario:

        return jsonify({
            "mensaje": "Hola Mundo Backend",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre_completo,
                "correo": usuario.correo_institucional
            }
        })

    return jsonify({
        "mensaje": "Hola Mundo Backend",
        "usuario": None
    })

# ==========================================
# Ejecutar servidor
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)