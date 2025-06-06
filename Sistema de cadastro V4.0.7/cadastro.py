from flask import Blueprint, request, redirect, url_for, flash, session, render_template  # type: ignore
from emailEnvio import enviar_codigo_autenticacao # type: ignore
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
import random

criar_bp_cad = Blueprint("cadastrar", __name__, template_folder="templates")
cliente = MongoClient("localhost", 27017)

db = cliente.database_Mvkit 

def gerar_senha():
    return str(random.randint(100000, 999999))

def validacao_entrega():
    return str(random.randint(1000, 9999))

table = db.usuario

@criar_bp_cad.route("/cadastrar", methods=["POST"])
def cadastro():
    email = request.form["email"]
    codigo = enviar_codigo_autenticacao(email)
    if not codigo:
        return "Erro ao enviar o código de autenticação. Tente novamente.", 500
    usuario_existente = table.find_one({"email": email})
    session.clear()
    session['email'] = email
    session['codigo_autenticacao'] = codigo
    if usuario_existente:
        print("Email já cadastrado")
        return redirect("/sms")
    email_id = table.insert_one({'email': email}).inserted_id
    session['usuario_id'] = str(email_id)
    print("sucesso")
    return redirect("/sms")

@criar_bp_cad.route("/cadastrarnum", methods=["POST"])
def cadastronum():
    numero = request.form["numero"]
    usuario_existente = table.find_one({"numero": numero})
    nova_senha = gerar_senha()
    if usuario_existente:
        print("Número já cadastrado")
        session.clear()
        session['numero'] = numero
        session['senha'] = str(nova_senha)
        return redirect("/sms")  
    numero_id = table.insert_one({"numero": numero}).inserted_id
    session.clear()
    session['senha'] = str(nova_senha)
    session['usuario_id'] = str(numero_id)
    session['numero'] = numero
    print("Cadastro realizado com sucesso")
    return redirect("/sms")

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
        return redirect('/')
    return redirect("/perfil")

@criar_bp_cad.route("/delete_cad", methods=["POST"])
def delete():
    try:
        if session['email']:
            table.delete_one({"email": session['email']})
            session.clear()
            return redirect("/")
        else:
            table.delete_one({"numero": session['numero']})
            session.clear()
            return redirect("/")
    except:
        return redirect("/meusdados")
    
@criar_bp_cad.route("/salvarCard", methods=["POST"])
def salvar_cartao():
    nome_cartao = request.form.get("nome_cartao")
    numero_cartao = request.form.get("numero_cartao")
    validade_cartao = request.form.get("validade_cartao")
    cvv = request.form.get("cvv")
    forma_pagamento = request.form.get("forma_pagamento")

    cartao = {
        "nome": nome_cartao,
        "numero": numero_cartao,
        "validade": validade_cartao,
        "cvv": cvv,
        "forma_pagamento": forma_pagamento
    }

    try:
        if session.get('email'):
            table.update_one({"email": session['email']}, {"$set": {"cartao": cartao}})
        elif session.get('numero'):
            table.update_one({"numero": session['numero']}, {"$set": {"cartao": cartao}})
        else:
            return "Usuário não autenticado", 401

        return redirect("/pagamento")  # ✅ Redireciona após salvar com sucesso

    except Exception as e:
        print("Erro ao salvar cartão:", e)
        return "Erro interno ao salvar cartão", 500
