from flask import Blueprint, request, redirect


armz = Blueprint("armazenar", __name__, template_folder="templates")

@armz.route("/guardar", methods=["POST"])
def armazenar():
    try:
        code_str = "".join(request.form.getlist("cod_auth"))
        code = int(code_str)
    except ValueError:
        return "Erro: cod_auth deve ser um número inteiro", 400
    if code == 111111:
        print("Sucesso")
        return redirect("/sucesso")
    else:
        print("falhou :(") 



#### ROTA
from flask import Flask, render_template, redirect, flash
from cadastro import criar_bp_cad, dados_cadastro
from armazem import armz

app = Flask(__name__)

app.register_blueprint(criar_bp_cad)
app.register_blueprint(armz)


class Routes():
    @app.route("/")
    def cad():
        return render_template("index.html")
    
    @app.route("/sucesso")
    def sucesso():
        return render_template("sucesso.html", data=dados_cadastro)
