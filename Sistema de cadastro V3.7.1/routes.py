from flask import Flask, render_template, redirect, url_for, flash, session # type: ignore
from authlib.integrations.flask_client import OAuth # type: ignore
from cadastro import criar_bp_cad, table
from endereco import endereco_local
from bson.objectid import ObjectId # type: ignore
from dotenv import load_dotenv
import secrets
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(endereco_local)
app.register_blueprint(criar_bp_cad)

# variáveis de ambiente
load_dotenv()
app.config["FACEBOOK_CLIENT_ID"] = os.getenv('FACEBOOK_CLIENT_ID')
app.config["FACEBOOK_CLIENT_SECRET"] = os.getenv('FACEBOOK_CLIENT_SECRET')
app.config["GOOGLE_CLIENT_ID"] = os.getenv('GOOGLE_CLIENT_ID')
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv('GOOGLE_CLIENT_SECRET')


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

google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
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

    @app.route("/login/google")
    def login_google():
        session["nonce"] = os.urandom(16).hex()
        return google.authorize_redirect(url_for("google_callback", _external=True))

    @app.route("/login/google/callback")
    def google_callback():
        try:
            token = google.authorize_access_token()
            if not token:
                return "Erro: Token não recebido", 400

            user_info = google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()

            if user_info:
                session["user"] = user_info
                return f"Login bem-sucedido! Bem-vindo, {user_info['name']}"

            return "Erro: Não foi possível obter informações do usuário", 401
        except Exception as e:
            return f"Erro no login: {str(e)}", 500