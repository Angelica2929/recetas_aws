from crypt import methods
from flask import render_template,redirect,session,request,flash #importaciones de modulos de flask
from flask_app import app

#Importando el modelO User

from flask_app.models.users import User

#Importando el modelo Messahe
from flask_app.models.recipes import Recipe

#Importando el Bcript
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)#inicializando instancia bcrypt

@app.route('/')
def index():
    return render_template('index.html')

#Creando una ruta para register

@app.route('/register', methods=['POST'])
def register():
    #request.form={
    # "first_name:"Elena",
    # "last_name":"De troya",
    # "email":"elana@coding.com",
    # "password":"12345"}
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password']) #encripta password y lo pone en variable pwd
    formulario = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":pwd
    }
    id=User.save(formulario)#Guardando a mi usuario y recibo el ID del nuevo registro
    session['user_id']=id#Guardando en sesion el identificador

    return redirect('/wall')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("E-mail no encontrado",'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Password Incorrecto",'login')
        return redirect('/')
    session['user_id']=user.id
    return redirect('/wall')

@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        "id":session['user_id']
    }
    user = User.get_by_id(formulario) #Usuario que inicio sesion
    recipes = Recipe.get_all() #Recibimos lista de recetas
 
    return render_template('wall.html',user=user,recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()#elimina sesion
    return redirect('/')
