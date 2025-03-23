from flask import Blueprint, request, redirect, url_for, flash, session   # type: ignore
from routes import table
authentic = Blueprint("authentic", __name__, template_folder="templates")

@authentic.route("/auth", methods=["POST"])
def auth():
    sms1 = request.form["sms1"]
    sms2 = request.form["sms2"]
    sms3 = request.form["sms3"]
    sms4 = request.form["sms4"]
    sms5 = request.form["sms5"]
    sms6 = request.form["sms6"]
    code = sms1 + sms2 + sms3 + sms4 + sms5 + sms6
    try:
        if code == session['senha']:
            session.pop('senha', None)
            print("Daqui passou")
            try:
                email = table.find_one({'email': session['email']})
                if 'endereco' in email:
                    session.pop('cep', None)
                    session['cep'] = 'cep' in email['endereco']
                    return redirect("/meusdados")
                else:
                    return redirect("/cadastro_local")
            except:
                num = table.find_one({'numero': session['numero']})
                if 'endereco' in num:
                    session.pop('cep', None)
                    session['cep'] = 'cep' in num['endereco']
                    return redirect("/meusdados")
                else:
                    return redirect("/cadastro_local")
    except:
        print("Erro ainda desconhecido")
        return redirect("/")