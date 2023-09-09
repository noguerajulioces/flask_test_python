import os
from flask import session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuarios import Usuario

class Banda:
  def __init__(self, data) -> None:
    self.id = data['id']
    self.nombre = data['nombre']
    self.socio_fundador = data['socio_fundador']
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
    print(os.getenv('BASE_DATOS'))
    print('Resultados de la consulta:', resultados)
    for banda in resultados:
      bandas.append(cls(banda))

    return bandas

  @classmethod
  def save(cls, data):
    query = "INSERT INTO bandas (nombre, socio_fundador, genero) VALUES (%(nombre)s, %(socio_fundador)s, %(genero)s);"
    return connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)


  @classmethod
  def get(cls, id ):
    query = "SELECT * FROM bandas WHERE id = %(id)s;"
    data = { 'id': id }
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    if resultados:
      return cls(resultados[0])

    return None


  @classmethod
  def eliminar(cls, id ):
    query = "DELETE FROM bandas WHERE id = %(id)s;"
    data = { 'id': id }
    connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    return True

  def delete(self):
    query = "DELETE FROM bandas WHERE id = %(id)s;"
    data = { 'id': self.id }
    connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    return True
