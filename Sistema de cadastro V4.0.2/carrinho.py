from flask import Blueprint, redirect, request, session, render_template, url_for # type: ignore
from cadrestaurante import table_user

carrinho_bp = Blueprint("carrinho", __name__, template_folder="templates")

@carrinho_bp.route("/add_cart", methods=["POST"])
def add_cart():
    produto = request.form["teste"]
    novo_produto = {"Produto": produto, "Valor": 10, "Quantidade": 1}
    if 'carrinho' not in session:
        session['carrinho'] = []
    carrinho = session['carrinho']
    carrinho.append(novo_produto)
    session['carrinho'] = carrinho

    return redirect("/teste_carrinho")

@carrinho_bp.route("/remove_item/<int:index>", methods=["POST"])
def remove_item(index):
    carrinho = session.get("carrinho", [])
    if 0 <= index < len(carrinho):
        carrinho.pop(index)
        session['carrinho'] = carrinho
    return redirect("/teste_carrinho")
