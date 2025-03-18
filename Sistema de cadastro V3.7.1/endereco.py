from flask import Blueprint, redirect, request, session, render_template # type: ignore
from cadastro import table


endereco_local = Blueprint("endereco_local", __name__, template_folder="templates")


@endereco_local.route("/endereco", methods=["POST"])
def data():
    name = request.form.get("name")
    cpf = request.form.get("cpf")
    cep = request.form.get("cep")
    bairro = request.form.get("bairro")
    rua = request.form.get("rua")
    cidade = request.form.get("cidade")
    estado = request.form.get("uf")
    num_casa = request.form.get("number")
    try:
        if session['usuario_id']:
            local = {"name": name,"cpf": cpf,"cep": cep, "bairro": bairro, "rua": rua, "cidade": cidade, "estado": estado, "numero_casa": num_casa}
            endereco = {"$set": {"endereco": local}}
            try:
                if session.get('email'):
                    table.update_one({"email": session['email']}, endereco)
                    return redirect('/')
                elif session.get('numero'):
                    table.update_one({"numero": session['numero']}, endereco)
                    print("Funcionou")
                    return redirect("/")
            except:
                print("Erro")
    except:
        if session['email'] or session['numero']:
            local = {"name": name,"cpf": cpf,"cep": cep, "bairro": bairro, "rua": rua, "cidade": cidade, "estado": estado, "numero_casa": num_casa}
            endereco = {"$set": {"endereco": local}}
            try:
                if session.get('email'):
                    table.update_one({"email": session['email']}, endereco)
                    return redirect('/')
                elif session.get('numero'):
                    table.update_one({"numero": session['numero']}, endereco)
                    print("Funcionou")
                    return redirect("/")
            except:
                print("Erro")


@endereco_local.route("/meusdados", methods=["GET"])
def dataread():
    try:
        if session['email']:
            mydata = table.find_one({'email':session['email']})
            pass
        else:
            print("Erro, você não tem um cadastro!")
            return redirect("/")
    except:
        if session['numero']:
            mydata = table.find_one({'numero':session['numero']})
            pass
        else:
            print("Erro, você não tem um cadastro!")
            return redirect("/")

    return render_template("meusdados.html",meusdados = mydata)

@endereco_local.route("/del_dados", methods=["POST"])
def deleter_dados():
    if 'email' in session:
        table.update_one({'email':session['email']}, {'$unset':{"endereco":1}})
        return redirect('/')
    elif 'numero' in session:
        table.update_one({'numero':session['numero']}, {'$unset':{"endereco":1}})
        return redirect('/')
    else:
        print('Erro não foi encontado nenhuma informação para ser deletada')

