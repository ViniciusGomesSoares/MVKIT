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
