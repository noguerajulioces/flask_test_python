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
        "socio_fundador": session['usuario'],
        "genero": request.form['genero'],
        "origen": request.form['origen']
    }
    Banda.save(data)
    return redirect('/')
  return render_template('nueva_banda.html')
