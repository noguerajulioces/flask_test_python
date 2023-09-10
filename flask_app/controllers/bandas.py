from flask import flash, redirect, request, session, render_template
from flask_app.models.bandas import Banda
from flask_app.models.usuarios import Usuario

from flask_app import app

# Route para renderizar nueva banda formulario
@app.route('/nueva_banda', methods=['GET', 'POST'])
def nueva_banda():
  if request.method == 'POST':
    data = {
        "nombre": request.form['nombre'],
        "socio_fundador": session['usuario']['id'],
        "genero": request.form['genero'],
        "origen": request.form['origen']
    }
    Banda.save(data)
    return redirect('/')
  return render_template('nueva_banda.html')


# Route para renderizar mis banddas
@app.route('/mis_bandas', methods=['GET'])
def mis_bandas():
  usuario_id = session['usuario']['id']
  bandas = Banda.get_bandas_by_usuario(usuario_id)
  return render_template('mis_bandas.html', bandas=bandas)

@app.route('/bandas/<int:banda_id>/editar', methods=['GET'])
def editar_banda(banda_id):
  banda = Banda.get(banda_id)
  return render_template('editar_banda.html', banda=banda)

@app.route('/bandas/<int:banda_id>/editar', methods=['POST'])
def actualizar_banda(banda_id):
  data = {
    "id": banda_id,
    "nombre": request.form['nombre'],
    "socio_fundador": session['usuario']['id'],
    "genero": request.form['genero'],
    "origen": request.form['origen'],
  }
  Banda.update(data)
  return redirect('/mis_bandas')

@app.route('/bandas/<int:banda_id>/eliminar', methods=['POST'])
def eliminar_banda(banda_id):
  Banda.eliminar(banda_id)
  current_url = request.referrer
  if current_url.endswith('/'):
    return redirect('/')
  else:
    return redirect('/mis_bandas')



