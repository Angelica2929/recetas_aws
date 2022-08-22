from flask import Flask

app = Flask(__name__)

#Generar la secret_key
app.secret_key = "Soy la mejor"