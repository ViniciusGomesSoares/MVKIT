from flask import Blueprint, request, redirect, url_for, flash, jsonify # type: ignore
from pymongo import MongoClient # type: ignore
import random


criar_bp_cad = Blueprint("cadastrar", __name__, template_folder="templates")
cliente = MongoClient("localhost", 27017)

db = cliente.database_Mvkit 

table = db.usuario

def gerar_senha():
    return str(random.randint(100000, 999999))  # Exemplo: 482731


@criar_bp_cad.route("/cadastrar", methods=["POST"])
def cadastro():
    email = request.form["email"]
    usuario_existente = table.find_one({"email": email})
    nova_senha = gerar_senha()
    if usuario_existente:  
        print("Email já cadastrado")
        return redirect("/") 
    table.insert_one({'email': email, "senha": nova_senha})

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


@criar_bp_cad.route("/update", methods=["POST"])
def update():
    email = request.form["email"]
    usuario_existente = table.find_one({"email": email})
    email_novo = request.form["email_edit"]
    if usuario_existente:
        table.update_one(
            {"email": email},
            {"$set": {"email": email_novo}}
        )
    else:
        return jsonify({"erro": "Email não encontrado no banco de dados!"})


    return redirect("/perfil")


#aqui fiz duas formas de gerar um sms/senha, um no formato string e outra no formato int vamos conversar depois qual seria melhor para nosso projeto


# @criar_bp_cad.route("/gerar_senha", methods=["POST"])
# def gerar_senha_para_email():

#     def gerar_senha():
#         return str(random.randint(100000, 999999))  # Exemplo: 482731

#     email = request.form.get("email")

#     if not email:
#         return jsonify({"erro": "O campo 'email' é obrigatório!"}), 400

#     usuario_existente = table.find_one({"email": email})

#     if not usuario_existente:
#         return jsonify({"erro": "Email não encontrado no banco de dados!"}), 404

    

    

#     return jsonify({"mensagem": "Senha gerada com sucesso!", "senha": nova_senha}), redirect("/perfil")