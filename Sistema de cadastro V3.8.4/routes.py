from flask import Flask, render_template, redirect, url_for, flash, session, send_file, Response # type: ignore
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId # type: ignore
import os
from authlib.integrations.flask_client import OAuth # type: ignore
import secrets
from endereco import endereco_local
from authy import authentic
from dotenv import load_dotenv # type: ignore
import random
from cadrestaurante import bp_restauranteadmin, table_user
import base64

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(endereco_local)
app.register_blueprint(criar_bp_cad)
app.register_blueprint(authentic)
app.register_blueprint(bp_restauranteadmin)

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
    authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
    access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
    client_kwargs={"scope": "email"},
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
    def get_imagem():
        if 'email' not in session:
            return redirect('/login_restaurante')
        usuario = table_user.find_one({"email": session['email']})
        if not usuario or "imagem" not in usuario:
            return render_template("perfiladm.html")
        imagem_binaria = usuario["imagem"]
        imagem_base64 = base64.b64encode(imagem_binaria).decode('utf-8')
        return render_template("perfiladm.html", imagem_url=f"data:image/jpeg;base64,{imagem_base64}", email = session['email'])
    
    @app.route("/produtos")
    def produtos():
        if 'email' not in session:
            return redirect('/login_restaurante')
        produtos = table_user.find_one({"email": session['email']})
        produtos_lista = produtos["produtos"]
        for n in produtos_lista:
            imagem_binaria = n["imagem"]
        imagem_base64 = base64.b64encode(imagem_binaria).decode('utf-8')

        return render_template("produtos.html", produtos = produtos_lista, imagem_url=f"data:image/jpeg;base64,{imagem_base64}")
    
    @app.route("/" + str(random.randint(100000, 999999)))
    def base_adm():
        return render_template("base_adm_profile.html")
    
    @app.route("/login_restaurante")
    def login_restaurante():
        return render_template("loginRestaurante.html")
    
    @app.route("/gestao_restaurante")
    def gestao_restaurante():
        if 'email' not in session:
            return redirect('/login_restaurante')
        restaurante = table_user.find_one({"email": session['email']})
        restaurante_lista = restaurante["restaurante"]

        return render_template("gestao_restaurante.html",  restaurante = restaurante_lista)