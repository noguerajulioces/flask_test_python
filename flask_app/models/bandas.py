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
    self.usuarios_ids = data['usuarios_ids']

  def __str__(self) -> str:
    return f"{self.nombre}"  # Cambiado de self.banda a self.nombre

  @classmethod
  def get_all(cls):
    query = """
    SELECT
      bandas.id AS id,
      bandas.nombre AS nombre,
      bandas.genero AS genero,
      bandas.origen AS origen,
      usuarios.nombre AS fundador_id,
      GROUP_CONCAT(usuarios_has_bandas.usuario_id) AS usuarios_ids
    FROM
      bandas
    JOIN
      usuarios ON bandas.fundador_id = usuarios.id
    LEFT JOIN
      usuarios_has_bandas ON bandas.id = usuarios_has_bandas.banda_id
    GROUP BY
      bandas.id;
    """
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)

    bandas = []
    for resultado in resultados:
      banda = cls({
        'id': resultado['id'],
        'nombre': resultado['nombre'],
        'origen': resultado['origen'],
        'genero': resultado['genero'],
        'fundador_id': resultado['fundador_id'],
        'usuarios_ids': resultado['usuarios_ids']
      })
      bandas.append(banda)

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

  @classmethod
  def eliminar_relacion(cls, banda_id):
    query = "DELETE FROM usuarios_has_bandas WHERE banda_id = %(banda_id)s AND usuario_id = %(usuario_id)s"
    data = {
        'banda_id': banda_id,
        'usuario_id': session['usuario']['id'],
    }
    connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
    return True

  @classmethod
  def agregar_relacion(cls, banda_id):
    query = "INSERT INTO usuarios_has_bandas (banda_id, usuario_id) VALUES (%(banda_id)s, %(usuario_id)s)"
    data = {
        'banda_id': banda_id,
        'usuario_id': session['usuario']['id'],
    }
    connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
    return True


  @classmethod
  def get_bandas_usuario(cls, usuario_id):
    query = """
    SELECT
      bandas.id AS banda_id,
      bandas.nombre AS banda_nombre
      -- Aquí deberías agregar la selección del campo 'genero' si deseas usarlo más tarde en tu código Python
    FROM
      usuarios_has_bandas
    JOIN
      bandas ON usuarios_has_bandas.banda_id = bandas.id
    WHERE
      usuarios_has_bandas.usuario_id = %(usuario_id)s;
    """
    data = {'usuario_id': usuario_id}
    resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

    bandas = []
    for resultado in resultados:
      banda = {
        'id': resultado['banda_id'],
        'nombre': resultado['banda_nombre'],
        # 'genero': resultado['banda_genero']  # Este campo no está siendo seleccionado en tu consulta SQL
      }
      bandas.append(banda)
    return bandas


@classmethod
def usuario_esta_en_banda(cls, usuario_id, banda_id):
  query = """
  SELECT
    *
  FROM
    usuarios_has_bandas
  WHERE
    usuarios_has_bandas.usuario_id = %(usuario_id)s
    AND usuarios_has_bandas.banda_id = %(banda_id)s;
  """
  data = {'usuario_id': usuario_id, 'banda_id': banda_id}
  resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)

  return len(resultados) > 0

