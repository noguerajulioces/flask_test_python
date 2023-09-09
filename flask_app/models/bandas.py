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
    self.usuario_id = data['usuario_id']
    self.usuario = None


  def __str__(self) -> str:
    return f"{self.banda}"

  @classmethod
  def validar(cls, formulario):

    errores = []

    if len(formulario['Banda']) == 0:
        errores.append(
            "Este campo es obligatorio"
        )

    if len(formulario['Banda']) < 2:
        errores.append(
            "La banda debe tener al menos 2 caracteres"
        )

    return errores

  @classmethod
  def get_all(cls):
    resultados_instancias = []
    query = "SELECT * FROM bandas join usuarios ON bandas.usuario_id = usuarios.id"
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
    for resultado in resultados:
      print(resultado)
      instancia = cls(resultado)

      data = {
        'id': resultado['usuarios.id'],
        'nombre': resultado['nombre'],
        'apellido': resultado['apellido'],
        'email': resultado['email'],
        'password': resultado['password'],
        'created_at': resultado['usuarios.created_at'],
        'updated_at': resultado['usuarios.updated_at'],
      }

      instancia.usuario = Usuario(data)

      resultados_instancias.append(instancia)

    return resultados_instancias

  @classmethod
  def get_all_facil(cls):
    resultados_instancias = []
    query = "SELECT * FROM bandas"
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
    for resultado in resultados:
        print(resultado)
        instancia = cls(resultado)
        instancia.usuario = Usuario.get(instancia['usuario_id'])
        resultados_instancias.append(instancia)

    return resultados_instancias

  @classmethod
  def save(cls, data ):
    query = "INSERT INTO `bandas` (`id`,`nombre`,`socio_fundador`,`genero`) VALUES (%(id)s, %(nombre)s, %(socio_fundador)s, %(genero)s);"
    data_con_usuario = {
        **data,
        'usuario_id': session['usuario']['id'],
    }

    return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data_con_usuario )

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
