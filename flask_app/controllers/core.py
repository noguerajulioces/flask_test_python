from flask import render_template, flash, redirect, session
from flask_app import app
from flask_app.models.bandas import Banda

@app.route('/')
def inicio():
  if 'usuario' not in session:
    flash("no estás logeado!!!!", "error")
    return redirect("/login")


  return render_template(
    'inicio.html'
  )
