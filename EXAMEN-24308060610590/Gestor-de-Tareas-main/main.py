from flask import Flask, flash, render_template, request, redirect, send_file, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "rayos_de_orbita"

client = MongoClient("mongodb://localhost:27017/")
db = client["24308060610590"]
usuarios_collection = db["usuarios"]

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        usuario = usuarios_collection.find_one({
            "email": email,
            "password": password
        })

        if usuario:
            session["usuario"] = email
            session["nombre"] = usuario["nombre"]  
            flash("Inicio de sesión exitoso")
            return redirect("/index")
        else:
            flash("Correo o contraseña incorrectos")
            return redirect("/login")
    return render_template("login.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        edad = request.form.get("edad")
        genero = request.form.get("genero")

        if usuarios_collection.find_one({"email": email}):
            flash("El correo ya está registrado")
            return redirect("/registrar")

        if usuarios_collection.find_one({"nombre": nombre}):
            flash("El nombre de usuario ya está en uso")
            return redirect("/registrar")

        if usuarios_collection.find_one({
            "nombre": nombre,
            "edad": edad,
            "genero": genero
        }):
            flash("Este usuario ya está registrado con esos datos")
            return redirect("/registrar")

        usuarios_collection.insert_one({
            "nombre": nombre,
            "email": email,
            "password": password,
            "edad": edad,
            "genero": genero
        })

        session["usuario"] = email  
        session["nombre"] = nombre  
        flash("Registro exitoso")
        return redirect("/index")

    return render_template("registro.html")

@app.route("/index")
def index():
    
    if "usuario" not in session:
        return redirect("/login")
    
    nombre = session.get("nombre")  
    return render_template("index.html", nombre=nombre)

@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        flash("Sesión no iniciada. Por favor inicia sesión.", "warning")
        return redirect(url_for("login"))
    
    nombre = session.get("nombre")  
    return render_template("perfil.html", nombre=nombre)

@app.route("/logout")
def logout():
    session.clear() 
    flash("Sesión cerrada correctamente")
    return redirect(url_for("login"))

@app.route("/recuperar")
def recuperar():
    return render_template("recuperar.html")

@app.route("/agregar", methods=["POST"])
def agregar():
    return redirect("/tareas")

@app.route("/privacidad")
def privacidad():
    return send_file("static/OrbitRay_Privacidad.docx", as_attachment=True)

@app.route("/terminos")
def terminos():
    return send_file("static/OrbitRay_Terminos.docx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)