from flask import Flask, render_template, redirect, url_for, flash, session # type: ignore
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId # type: ignore
import os
from authlib.integrations.flask_client import OAuth # type: ignore
import secrets
from endereco import endereco_local

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(endereco_local)
app.register_blueprint(criar_bp_cad)

# variáveis de ambiente
app.config["FACEBOOK_CLIENT_ID"] =  "1814037189370814"
app.config["FACEBOOK_CLIENT_SECRET"] = "c7ca0bf4561e7faa29547976bd08ca76"

oauth = OAuth(app)


facebook = oauth.register(
    name="facebook",
    client_id=app.config["FACEBOOK_CLIENT_ID"],
    client_secret=app.config["FACEBOOK_CLIENT_SECRET"],
    authorize_url="https://www.facebook.com/dialog/oauth",
    authorize_params={"scope": "email"},
    access_token_url="https://graph.facebook.com/oauth/access_token",
    access_token_params=None,
    client_kwargs={"scope": "email"},
    api_base_url="https://graph.facebook.com/",
)

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
    
    @app.route('/update')
    def perfil():
        return render_template("update_email.html")
    
    @app.route('/teste')
    def testel():
        return render_template("teste.html")
    @app.route('/sms')
    def sms():
        notify = session['senha']
        return render_template("sms.html", senha = notify)
    
    @app.route("/login/facebook")
    def login_facebook():
        return facebook.authorize_redirect(url_for('facebook_callback', _external=True))

    @app.route("/login/facebook/callback")
    def facebook_callback():
        try:
            token = facebook.authorize_access_token()
            user_info = facebook.get("me?fields=id,name,email").json()
            session["user"] = user_info  # armazenei o usuário na sessão
            return print(user_info)  # isso exibe os dados (mudar para redirecionamento depois)
        except Exception as e:
            return f"Erro no login: {str(e)}", 500