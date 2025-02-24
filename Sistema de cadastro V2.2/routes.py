from flask import Flask, render_template, redirect, url_for, flash # type: ignore
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId


app = Flask(__name__)


app.register_blueprint(criar_bp_cad)


class Routes():
    @app.route("/")
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
        # deleta o dado incerido
        table.delete_one({'_id':ObjectId(id)})
        return redirect('/delete')