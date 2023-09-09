from flask import flash, redirect, request, session, render_template
from flask_app.models.bandas import Banda
from flask_app.models.usuarios import Usuario

from flask_app import app


@app.route('/procesar_bandas', methods=["POST"])
def procesar_pensamiento():
    print(request.form)

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")


    errores = Banda.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/")

    Banda.save(request.form)
    flash("pensamiento agregado", "success")
    return redirect("/")

@app.route('/pensamiento/<int:id>/eliminar')
def pensamiento_eliminar(id):
    Pensamiento.eliminar(id)
    flash("pensamiento eliminado!", "success")
    return redirect("/")


@app.route('/usuario/<int:id>')
def usuario_pensamientos(id):
    usuario = Usuario.get(id)
    pensamientos_usuario = Pensamiento.get_by_usuario(id)
    return render_template("usuario.html", usuario=usuario, pensamientos=pensamientos_usuario)
