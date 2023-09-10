import os
from flask import session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuarios import Usuario

class Banda:
  def __init__(self, data) -> None:
    self.id = data['id']
    self.nombre = data['nombre']
    self.fundador_id = data['fundador_id']
    self.genero = data['genero']
    self.origin = data['origen']

  def __str__(self) -> str:
    return f"{self.nombre}"  # Cambiado de self.banda a self.nombre

  @classmethod
  def get_all(cls):
    bandas = []
    query = "SELECT * FROM bandas"
    conexion = connectToMySQL(os.getenv('BASE_DATOS'))
    resultados = conexion.query_db(query)
    print('Resultados de la consulta:', resultados)
    for banda in resultados:
      bandas.append(cls(banda))

    return bandas

  @classmethod
  def save(cls, data):
    query = "INSERT INTO bandas (nombre, fundador_id, genero) VALUES (%(nombre)s, %(fundador_id)s, %(genero)s);"
    return connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)


  @classmethod
  def get_bandas_by_usuario(cls, usuario_id):
    query = "SELECT * FROM bandas WHERE fundador_id = %(usuario_id)s;"
    data = {"usuario_id": usuario_id}
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

    bandas = []
    for resultado in resultados:
      bandas.append(cls(resultado))

    return bandas

  @classmethod
  def get(cls, banda_id):
    query = "SELECT * FROM bandas WHERE id = %(banda_id)s;"
    data = {"banda_id": banda_id}
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

    if resultados:
        return cls(resultados[0])
    else:
        return None

  @classmethod
  def update(cls, data):
    query = """
      UPDATE bandas
      SET nombre = %(nombre)s, genero = %(genero)s, origen = %(origen)s
      WHERE id = %(id)s;
    """
    return connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

  @classmethod
  def eliminar(cls, banda_id):
    query = "DELETE FROM bandas WHERE id = %(banda_id)s;"
    data = {"banda_id": banda_id}
    connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)


  def delete(self):
    query = "DELETE FROM bandas WHERE id = %(id)s;"
    data = { 'id': self.id }
    connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    return True
