from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.usuarios import Usuario
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  


#de inicio de sesion, verifica si el usuario ya inicio sesion
@app.route('/login')
def registro():

    if 'usuario' in session:
        flash("Haz iniciado sesion" + session['usuario']['email'], "info")
        return redirect("/")

    return render_template("login.html")

#formulario de inicio de sesion, comprueba los datos del usuario en la bd y que coincida la contrasenha ingresada
@app.route('/procesar_login', methods=["POST"])
def procesar_login():
    print(request.form)

    usuario  = Usuario.get_by_email(request.form['email'])
    if not usuario:
        flash("el correo o la contraseña no es válida", "error")
        return redirect("/login")
    
    resultado = bcrypt.check_password_hash(usuario.password, request.form['password'])
    #si el dato hasheado coincide con lo que esta en la bd, se dirige a la ruta base
    if resultado:
        session['usuario'] = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email
        }
        return redirect("/")

    flash("la contraseña o el correo no es válido", "error")
    return redirect("/login")

#procesa el registro y da las validaciones de largor, etc 
@app.route('/procesar_registro', methods=["POST"])
def procesar_registro():
    # Imprimir el contenido del formulario en la consola para depuración
    print(request.form)

    # Validar los datos del formulario utilizando la función 'validar' de la clase 'Usuario'
    errores = Usuario.validar(request.form)

    # Si se encuentran errores de validación, mostrarlos y redirigir al formulario de registro
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/login")

    # Verificar que las contraseñas ingresadas coincidan
    if request.form["password"] != request.form["confirmar_password"]:
        flash("las contraseñas no son iguales", "error")
        return redirect("/login")

    # Crear un diccionario 'data' con los datos del usuario a registrar
    data = {
        'nombre': request.form["nombre"],
        'apellido': request.form["apellido"],
        'email': request.form["email"],
        'password': bcrypt.generate_password_hash(request.form["password"])  # Hashear la contraseña
    }

    # Guardar el usuario en la base de datos y obtener su ID
    id = Usuario.save(data)

    # Mostrar un mensaje de éxito y redirigir al formulario de inicio de sesión
    flash("Usuario registrado correctamente", "success")
    return redirect("/login")

#ruta que redirige al formulario de registro
@app.route('/salir')
def salir():
    session.clear()
    return redirect("/login")
