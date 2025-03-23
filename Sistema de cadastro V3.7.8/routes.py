from flask import Flask, render_template, redirect, url_for, flash, session # type: ignore
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId # type: ignore
import os
from authlib.integrations.flask_client import OAuth # type: ignore
import secrets
from endereco import endereco_local
from authy import authentic
from dotenv import load_dotenv # type: ignore
import random
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(endereco_local)
app.register_blueprint(criar_bp_cad)
app.register_blueprint(authentic)

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
def gerar_senha():
    return str(random.randint(100000, 999999))

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
    
    @app.route('/cadastro_local')
    def testel():
        return render_template("cadlocal.html")
    
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
            return redirect('/')  # isso exibe os dados (mudar para redirecionamento depois)
        except Exception as e:
            return f"Erro no login: {str(e)}", 500
        
    @app.route("/confirm_del")
    def confirmation():
        return render_template("confirm_del.html")
    @app.route("/login/google")
    def login_google():
        session["nonce"] = os.urandom(16).hex()
        return google.authorize_redirect(url_for("google_callback", _external=True))

    @app.route("/login/google/callback")
    def google_callback():
        try:
            token = google.authorize_access_token()
            if not token:
                return "Erro: Token não recebido", 500

            user_info = google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()
            
            try:
                if user_info:
                    nova_senha = gerar_senha()
                    session["user"] = user_info
                    email_user = user_info['email']
                    usuario_existente = table.find_one({"email": email_user})
                    if usuario_existente:
                        session.clear()
                        session['senha'] = str(nova_senha)
                        session['email'] = email_user
                        return redirect('/sms')
                    session.clear()
                    session['senha'] = str(nova_senha)
                    session['email'] = email_user
                    table.insert_one({'email': email_user})
                    return redirect("/sms")
            except:
                print("Erro ainda desconhecido")
                return redirect('/')
        
        except Exception as e:
            return f"Erro no login: {str(e)}", 500
        
    @app.route("/admin_panel")
    def admpanel():
        return render_template("perfiladm.html")
    @app.route("/produtos")
    def produtos():
        return render_template("produtos.html")
    @app.route("/" + str(random.randint(100000, 999999)))
    def base_adm():
        return render_template("base_adm_profile.html")