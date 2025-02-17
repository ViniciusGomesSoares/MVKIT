from flask import Flask, request, redirect, render_template

app = Flask(__name__)

contas = [{"email":"vini@gmail.com","senha":"123456"}]

@app.route("/logar", methods=["POST"])
def get_dados():
    email_log = request.form.get("email")
    senha_log = request.form.get("password")

    for data in contas:
        if email_log == data["email"] and senha_log == data["senha"]:
            print("Login bem-sucedido!", "success")
            return redirect("/")
        else:
            print("Email ou senha incorretos. Tente novamente.", "error")

    return redirect("/")

@app.route("/")
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)