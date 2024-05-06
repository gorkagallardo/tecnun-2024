from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sqlite3
import re

app = Flask(__name__)
api = Api(app)

def validar_email(email):
    """Valida el formato del email usando una expresión regular."""
    patron_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return re.match(patron_email, email)

@app.route('/')
def hello_world():
    return 'Welcome to the new World!'

class Usuario(Resource):
    def get(self):
          # Conexión a la base de datos
        conexion = sqlite3.connect('/app/data/db.sqlite')
        cursor = conexion.cursor()
        
        # Ejecutar consulta SQL
        query = "SELECT id, name, email FROM users"
        resultado = cursor.execute(query)
        
        # Crear lista de diccionarios con los resultados
        usuarios = [
            {'id': row[0],'name': row[1], 'email': row[2]} for row in resultado.fetchall()
        ]
        
        # Cerrar la conexión con la base de datos
        cursor.close()
        conexion.close()
        
        # Devolver los resultados en formato JSON
        return jsonify(usuarios)
    def post(self):
        data = request.get_json()
        
        # Validación de la presencia de los campos necesarios
        if 'name' not in data or 'email' not in data:
            return {'error': 'Faltan campos requeridos: name, email'}, 400
        
        # Validación de que los campos no están vacíos
        if not all(data[k] for k in ['name', 'email']):
            return {'error': 'Ninguno de los campos puede estar vacio'}, 400
        
        # Validación del formato del email
        if not validar_email(data['email']):
            return {'error': 'Formato de email inválido'}, 400
        

        # Conexión a la base de datos y operaciones de inserción
        try:
            conexion = sqlite3.connect('/app/data/db.sqlite')
            cursor = conexion.cursor()
            query = 'INSERT INTO users (name, email) VALUES ( ?, ?)'
            cursor.execute(query, (data['name'], data['email']))
            conexion.commit()
        except sqlite3.IntegrityError:
            cursor.close()
            conexion.close()
            return {'error': 'El usuario ya existe'}, 409
        except Exception as e:
            cursor.close()
            conexion.close()
            return {'error': str(e)}, 500
        
        # Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()
        
        # Respuesta de éxito
        return {'mensaje': 'Usuario creado exitosamente'}, 201
    # def delete(self):
        # TODO

api.add_resource(Usuario, '/usuarios')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)