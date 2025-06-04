from flask import Blueprint, redirect, request, session, render_template, url_for # type: ignore


carrinho_bp = Blueprint("carrinho", __name__, template_folder="templates")

@carrinho_bp.route("/add_cart", methods=["POST"])
def add_cart():
    produto = request.form["name"]
    valor = float(request.form["valor"])
    novo_produto = {"Produto": produto, "Valor": valor, "Quantidade": 1}
    
    if 'carrinho' not in session:
        session['carrinho'] = []

    carrinho = session['carrinho']
    carrinho.append(novo_produto)
    session['carrinho'] = carrinho

    return redirect("/carrinho")

@carrinho_bp.route("/atualizar_quantidade/<int:index>", methods=["POST"])
def atualizar_quantidade(index):
    nova_qtd = int(request.form["quantidade"])

    if "carrinho" in session:
        carrinho = session["carrinho"]
        if 0 <= index < len(carrinho):
            carrinho[index]["Quantidade"] = nova_qtd
            session["carrinho"] = carrinho
            session.modified = True

    return redirect("/carrinho")

@carrinho_bp.route("/remove_item/<int:index>", methods=["POST"])
def remove_item(index):
    carrinho = session.get("carrinho", [])
    if 0 <= index < len(carrinho):
        carrinho.pop(index)
        session['carrinho'] = carrinho
    return redirect("/carrinho")

