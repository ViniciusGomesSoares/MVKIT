from flask import Blueprint, request, redirect, url_for, flash, session   # type: ignore
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
import random
from cadastro import db
from werkzeug.utils import secure_filename
from bson import Binary

bp_restauranteadmin = Blueprint("cadastrar_restaurante", __name__, template_folder="templates")

table_user = db.user_Admin

@bp_restauranteadmin.route("/cad_restaurante_user", methods=["POST"])
def cadastro_user():
    email = request.form["email"]
    usuario_existente = table_user.find_one({"email": email})
    if usuario_existente:  
        print("Email já cadastrado")
        session.clear()
        session['email'] = email
        return redirect("/admin_panel") 
    email_id = table_user.insert_one({'email': email}).inserted_id
    session.clear()
    session['usuario_id'] = str(email_id)
    session['email'] = email
    print("sucesso")
    return redirect("/admin_panel")

@bp_restauranteadmin.route("/cad_image", methods=["POST"])
def cad_image():
    if "email" not in session:
        return redirect("/login_restaurante")
    img = request.files["file_img"]
    if img.filename == "":
        flash("Nenhuma imagem selecionada!", "error")
        return redirect("/admin_panel")
    imagem_bytes = Binary(img.read())
    table_user.update_one(
        {"email": session["email"]},
        {"$set": {"imagem": imagem_bytes}}
    )
    flash("Imagem salva com sucesso!", "success")
    return redirect("/admin_panel")


@bp_restauranteadmin.route("/cad_restaurante", methods=["POST"])
def cadastro_restaurante():
    nome = request.form["nome"]
    endereco = request.form["endereco"]
    phone = request.form["phone"]
    url = request.form["url"]
    restaurante = {"nome": nome, "endereco": endereco, "telephone": phone, "url": url}
    restaurante_update = {"$set": {"restaurante": restaurante}}
    usuario = table_user.find_one({"email": session['email']})
    try:
        table_user.update_one({"email": usuario['email']}, restaurante_update)
        return redirect('/gestao_restaurante')
    except:
        print("Erro")
        return redirect('/admin_panel')

@bp_restauranteadmin.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect("/login_restaurante")

@bp_restauranteadmin.route("/cadastrar_prod", methods=["POST"])
def criar_produto():
    nome = request.form["name"]
    valor = request.form["valor"]
    categoria = request.form["categoria"]
    descricao = request.form["descricao"]
    
    img = request.files["file_img"]
    if img.filename == "":
        flash("Nenhuma imagem selecionada!", "error")
        return redirect("/admin_panel")
    imagem_bytes = Binary(img.read())
    
    produto = {
        "nome": nome,
        "valor": float(valor),
        "categoria": categoria,
        "descricao": descricao,
        "imagem": imagem_bytes
    }
    table_user.update_one(
        {"email": session["email"]},
        {"$push": {"produtos": produto}},
        upsert=True
    )
    return redirect("/produtos")
