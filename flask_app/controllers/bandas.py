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
