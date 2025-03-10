from flask import Flask, redirect, url_for, render_template, session, request, jsonify
from cadastro import criar_bp_cad, table
from bson.objectid import ObjectId
from authlib.integrations.flask_client import OAuth
import secrets
import os


app = Flask(__name__)

app.secret_key = "itStockSir"

# variáveis de ambiente
app.config["FACEBOOK_CLIENT_ID"] =  "1814037189370814"
app.config["FACEBOOK_CLIENT_SECRET"] = "c7ca0bf4561e7faa29547976bd08ca76"

oauth = OAuth(app)

app.register_blueprint(criar_bp_cad)



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

@app.route("/delete", methods=["POST", "GET"])
def deletar():
    usuarios = table.find()
    return render_template('delete.html', dados=usuarios)

@app.route('/<id>/delete/', methods=["POST"])
def delete(id):
    table.delete_one({'_id': ObjectId(id)})
    return redirect('/delete')

@app.route('/update')
def perfil():
    return render_template("update_email.html")



@app.route("/login/facebook")
def login_facebook():
    return facebook.authorize_redirect(url_for('facebook_callback', _external=True))

@app.route("/login/facebook/callback")
def facebook_callback():
    try:
        token = facebook.authorize_access_token()
        user_info = facebook.get("me?fields=id,name,email").json()
        session["user"] = user_info  # armazenei o usuário na sessão
        return jsonify(user_info)  # isso exibe os dados (mudar para redirecionamento depois)
    except Exception as e:
        return f"Erro no login: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
