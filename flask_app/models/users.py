from flask_app.config.mysqlconnection import connectToMySQL

import re #importamos expresiones regulares para verificar que tengamos el email con formato correcto

from flask import flash #mandar mensajes a la plantilla
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self , data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls,formulario):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        result=connectToMySQL('recetas').query_db(query,formulario) 
        return result
    @staticmethod
    def valida_usuario(formulario):
        #formulario={
        #  first_name: "Elena"
        # last_name:"De Troya"
        # email:elena@codingdojo,com
        # password:"password123"
        # confirm_password:"password123",
        # }
        es_valido = True
        #Valido que mi nombre tenga mas de 2 caracteres

        if len(formulario['first_name'])<3:
            flash('Nombre debe de tener al menos 3 caracteres','registro')
            es_valido=False
        
        if len(formulario['last_name'])<3:
            flash('Apellido debe de tener al menos 3 caracteres','registro')
            es_valido=False

        #Valido email con expresiones regulares

        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email invalido','registro')
            es_valido=False
        if len(formulario['password'])<6:
            flash('Contraseña debe tener al menos 6 caracteres','registro')
            es_valido=False

        if (formulario['password']) != formulario['confirm_password']:
            flash('Contraseñas no coinciden','registro')
            es_valido=False

        #Consulta si ya existe correo
        
        query = "SELECT*FROM users WHERE email =%(email)s"
        results=connectToMySQL('recetas').query_db(query,formulario)
        if len(results)>=1:
            flash('E-mail registrado previamente','registro')
            es_valido=False
        
        return es_valido

    @classmethod
    def get_by_email(cls,formulario):
        #formulario={
        # "email":"elena@coding.com"
        # "password":"12345"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result= connectToMySQL('recetas').query_db(query,formulario)
        if len(result)<1:
            return False
        else:
            user= cls(result[0])
            return user

    @classmethod
    def get_by_id(cls,formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario) #Select recibe lista
        user = cls(result[0])
        return user

    # @classmethod
    # def get_all(cls):
    #     query = " SELECT * FROM users"
    #     results = connectToMySQL('recetas').query_db(query)#recibe una lista de diccionarios
    #     #results=[
    #     #{id:1,first_name:Elena,......}
    #     #{id:2,first_name:Sofia,......}
    #     #]
    #     users=[] #lista vacia de usuarios
    #     for user in results:
    #         users.append(cls(user))#1crea instancia de usuario basado en el diccionario #2 agrega esa instancia a la lista de users
    #         return users
