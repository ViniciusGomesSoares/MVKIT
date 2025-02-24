from flask import Blueprint, request, redirect, url_for, flash   # type: ignore
from pymongo import MongoClient # type: ignore

criar_bp_cad = Blueprint("cadastrar", __name__, template_folder="templates")
cliente = MongoClient("localhost", 27017)

db = cliente.database_Mvkit 

table = db.usuario

@criar_bp_cad.route("/cadastrar", methods=["POST"])
def cadastro():
    email = request.form["email"]
    usuario_existente = table.find_one({"email": email})
    if usuario_existente:  
        print("Email já cadastrado")
        return redirect("/") 
    table.insert_one({'email': email})
    print("sucesso")
    
    return redirect("/")



@criar_bp_cad.route("/cadastrarnum", methods=["POST"])
def cadastronum():
    numero = request.form["numero"]
    usuario_existente = table.find_one({"numero": numero})
    if usuario_existente:
        print("Número já cadastrado")
        return redirect("/")  
    table.insert_one({"numero": numero})
    print("Cadastro realizado com sucesso")
    return redirect("/")




