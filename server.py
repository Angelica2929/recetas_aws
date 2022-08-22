from flask_app import app

#Importando Controlador
#pipenv install flask PyMySQL bcrypt
from flask_app.controllers import users_controller,recipes_controller

if __name__=="__main__":
    app.run(debug=True)