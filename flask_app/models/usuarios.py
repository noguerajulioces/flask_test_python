import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.expresiones_regulares import EMAIL_REGEX

# Definición de la clase Usuario
class Usuario:
    # Constructor de la clase y tiene none porque no retorna algo específico
    def __init__(self, data) -> None:
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    # Método especial para representar la instancia de la clase como una cadena, asi no toma como que es otra cosa y no me sale error
    def __str__(self) -> str:
        return f"{self.email} ({self.id})"

    # Método de clase para validar datos de un formulario, formulario es una variable que representa los datos del post y puede tener cualquier nombre
    @classmethod
    def validar(cls, formulario):
        errores = []

        # Validar el formato del correo electrónico utilizando una expresión regular
        if not EMAIL_REGEX.match(formulario['email']):
            errores.append("El correo indicado es inválido")

        # Verificar si el correo electrónico ya existe en la base de datos, comparando con la función de get_by_emaoil
        if cls.get_by_email(formulario['email']):
            errores.append("El correo ya existe")

        # Validar que el nombre tenga al menos 2 caracteres
        if len(formulario['nombre']) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")

        # Validar que el apellido tenga al menos 2 caracteres
        if len(formulario['apellido']) < 2:
            errores.append("El apellido debe tener al menos 2 caracteres")

        # Validar que la contraseña tenga al menos 8 caracteres
        if len(formulario['password']) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres")

        # Validar que todos los campos del formulario estén presentes
        for campo, valor in formulario.items():
            if len(valor) == 0:
                errores.append(f"{campo} no está presente. Dato obligatorio")

        return errores

    # Método de clase para obtener todos los usuarios
    @classmethod
    def get_all(cls):
        resultados_instancias = []
        query = "SELECT * FROM usuarios"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)

        # Crear instancias de Usuario a partir de los resultados y agregarlas a la lista
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    # Método de clase para guardar un nuevo usuario en la base de datos
    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

    # Método de clase para obtener un usuario por su ID
    @classmethod
    def get(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': id}
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    # Método de clase para obtener un usuario por su correo electrónico
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    # Método de clase para eliminar un usuario por su ID
    @classmethod
    def eliminar(cls, id):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = {'id': id}
        connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
        return True

    # Método para eliminar el objeto Usuario actual
    def delete(self):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
        return True

    # Método para actualizar los datos del objeto Usuario actual
    def update(self):
        query = "UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s, password = %(password)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'password': self.password,
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
        return True
