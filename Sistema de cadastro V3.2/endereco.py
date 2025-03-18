from flask import Blueprint, redirect, request, session # type: ignore
from cadastro import table


endereco_local = Blueprint("endereco_local", __name__, template_folder="templates")


@endereco_local.route("/endereco", methods=["POST"])
def data():
    cep = request.form.get("cep")
    bairro = request.form.get("bairro")
    rua = request.form.get("rua")
    cidade = request.form.get("cidade")
    estado = request.form.get("uf")
    num_casa = request.form.get("number")
    try:
        if session['usuario_id']:
            local = {"cep": cep, "bairro": bairro, "rua": rua, "cidade": cidade, "estado": estado, "numero_casa": num_casa}
            endereco = {"$set": {"endereco": local}}
            try:
                if session.get('email'):
                    table.update_one({"email": session['email']}, endereco)
                    return redirect('/teste')
                elif session.get('numero'):
                    table.update_one({"numero": session['numero']}, endereco)
                    print("Funcionou")
                    return redirect("/teste")
            except:
                print("Erro")
    except:
        if session['email']:
            local = {"cep": cep, "bairro": bairro, "rua": rua, "cidade": cidade, "estado": estado, "numero_casa": num_casa}
            endereco = {"$set": {"endereco": local}}
            try:
                if session.get('email'):
                    table.update_one({"email": session['email']}, endereco)
                    return redirect('/teste')
                elif session.get('numero'):
                    table.update_one({"numero": session['numero']}, endereco)
                    print("Funcionou")
                    return redirect("/teste")
            except:
                print("Erro")
    