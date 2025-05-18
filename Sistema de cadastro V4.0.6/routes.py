from flask import Flask, render_template, redirect, url_for, flash, session, send_file, Response, request # type: ignore
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
from carrinho import carrinho_bp

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(carrinho_bp)
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
        return render_template("sms.html")
    
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
        try:
            produtos = table_user.find_one({"email": session['email']})
            produtos_lista = produtos["produtos"]
            for n in produtos_lista:
                imagem_binaria = n["imagem"]
            imagem_base64 = base64.b64encode(imagem_binaria).decode('utf-8')
            return render_template("produtos.html", produtos = produtos_lista, imagem_url=f"data:image/jpeg;base64,{imagem_base64}")
        except:
            return render_template("produtos.html")
    
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

    @app.route("/editProduto")
    def editProduto():
        return render_template("editProduto.html")
    
    @app.route("/info_prod")
    def info_prod():
        return render_template("info_prod.html")
    
    @app.route("/carrinho")
    def teste_carrinho():
        try:
            carrinho = session["carrinho"]
            return render_template("carrinho.html", carrinho=carrinho)
        except:
            return render_template("carrinho.html", carrinho=[])

    @app.route("/pesquisa-produtos")
    def pesquisa_produto():
        restaurantes = table_user.find()

        lista_produtos = []

        for usuario in restaurantes:
            nome_restaurante = usuario.get("restaurante", {}).get("nome", "Restaurante sem nome")
            produtos = usuario.get("produtos", [])

            for produto in produtos:
                imagem_base64 = None
                if "imagem" in produto:
                    imagem_base64 = base64.b64encode(produto["imagem"]).decode("utf-8")
                
                lista_produtos.append({
                    "restaurante": nome_restaurante,
                    "nome": produto["nome"],
                    "valor": produto["valor"],
                    "categoria": produto["categoria"],
                    "descricao": produto["descricao"],
                    "imagem_base64": imagem_base64
                })

        return render_template("pesquisaProd.html", produtos=lista_produtos)

    @app.route("/frete", methods=["GET", "POST"])
    def opcoes_frete():
        fretes = [
            {
                "nome": "Entrega padrão",
                "tempo": "30-45",
                "descricao": "Seu pedido chegará sem custos adicionais dentro do prazo estimado.",
                "preco": 5,
                "selecionado": False
            },
            {
                "nome": "Entrega turbinada",
                "tempo": "15-25",
                "descricao": "Receba seu pedido mais rápido com nosso serviço prioritário.",
                "preco": 9.90,
                "selecionado": False 
            },
            {
                "nome": "Retirar no local",
                "tempo": "20",
                "descricao": "Economize o valor do frete retirando seu pedido pessoalmente.",
                "preco": 0,
                "selecionado": False
            }
        ]
        
        if request.method == "POST":
            frete_selecionado = request.form.get('frete')
            for frete in fretes:
                if frete['nome'] == frete_selecionado:
                    frete['selecionado'] = True
                else:
                    frete['selecionado'] = False

        return render_template("cards_frete.html", fretes=fretes)
    
    @app.route("/pagamento")
    def pagamento():
        carrinho = session.get("carrinho", [])
        subtotal = sum(item["Valor"] * item["Quantidade"] for item in carrinho)
        taxa_entrega = 0.00
        total = subtotal + taxa_entrega

        # Verificação de cartão salvo
        identificador = session.get("email") or session.get("numero")
        if not identificador:
            return redirect("/")

        filtro = {"email": session["email"]} if "email" in session else {"numero": session["numero"]}
        usuario = table.find_one(filtro)

        tem_cartao = False
        if usuario and "cartoes" in usuario and len(usuario["cartoes"]) > 0:
            tem_cartao = True

        return render_template("telaPagamento.html",
                            carrinho=carrinho,
                            subtotal=subtotal,
                            total=total,
                            tem_cartao=tem_cartao)

    @app.route("/cartao")
    def cartao():
        return render_template("telaCartao.html")
    
    @app.route("/acompanhamento")
    def acompanhamento():
        
        return render_template("acompanhamento.html")
    
    @app.route("/finalizar_pedido", methods=["POST"])
    def finalizar_pedido():

        carrinho = session.get("carrinho", [])
        if not carrinho:
            return "Carrinho vazio", 400

        subtotal = sum(item["Valor"] * item["Quantidade"] for item in carrinho)
        taxa_entrega = 0.00
        total = subtotal + taxa_entrega

        pedido = {
            "itens": carrinho,
            "subtotal": subtotal,
            "taxa_entrega": taxa_entrega,
            "total": total,
            "status": "Realizado"
        }

        try:
            if session.get('email'):
                table.update_one({"email": session['email']}, {"$push": {"pedidos": pedido}})
            elif session.get('numero'):
                table.update_one({"numero": session['numero']}, {"$push": {"pedidos": pedido}})
            else:
                return "Usuário não encontrado", 400

            # Limpa o carrinho após finalizar
            session.pop("carrinho", None)

            return redirect("/acompanhamento")

        except Exception as e:
            print("Erro ao salvar pedido:", e)
            return "Erro ao finalizar pedido", 500


    
