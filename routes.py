from flask import Flask, render_template, redirect, flash # type: ignore
from cadastro import criar_bp_cad


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