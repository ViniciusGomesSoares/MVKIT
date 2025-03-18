from flask import Flask, render_template, redirect, url_for, flash, session # type: ignore
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId # type: ignore
import os
from endereco import endereco_local

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(endereco_local)
app.register_blueprint(criar_bp_cad)


class Routes():
    @app.route("/")
    def main():
        return render_template("index.html")
    
    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/cadastronumero")
    def cadtel():
        return render_template("cadtel.html")

    @app.route("/cadastraremail")
    def cademail():
        return render_template("cademail.html")
    
    @app.route("/delete",methods=["POST","GET"])
    def deletar():
        usuarios = table.find()
        return render_template('delete.html', dados=usuarios) 
    
    @app.route('/<id>/delete/', methods=["POST"])
    def delete(id):
        table.delete_one({'_id':ObjectId(id)})
        return redirect('/')
    
    @app.route('/perfil')
    def perfil():
        return render_template("perfil.html")
    
    @app.route('/teste')
    def testel():
        return render_template("teste.html")
    @app.route('/sms')
    def sms():
        notify = session['senha']
        return render_template("sms.html", senha = notify)