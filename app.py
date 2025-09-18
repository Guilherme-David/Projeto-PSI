from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import secrets
from models import db, User, Produto, Sacola, ItemSacola, Pedido, ItemPedido
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import admin_required
from flask_migrate import Migrate

# ---------------- CONFIGURAÇÃO ----------------
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- LOGIN ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

@app.context_processor
def compartilhar_autenticado():
    return {"is_authenticated": current_user.is_authenticated}

# ---------------- ROTAS ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ROTAS DE AUTENTICAÇÃO
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "error")
            return redirect(url_for("register"))

        senha_hash = generate_password_hash(senha)
        user = User(email=email, senha_hash=senha_hash, is_admin=False)
        user.save()
        login_user(user)
        return redirect(url_for("cardapio"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha_hash, senha):
            login_user(user)
            return redirect(url_for("cardapio"))
        else:
            flash("Usuário ou senha incorretos.", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ROTAS DE PRODUTOS
@app.route("/cardapio")
@login_required
def cardapio():
    produtos = Produto.all()
    categorias = {"hamburguers": [], "sobremesas": [], "bebidas": []}
    for p in produtos:
        if p.categoria in categorias:
            categorias[p.categoria].append(p)
    return render_template("produtos.html", hamburguers=categorias["hamburguers"],
                           sobremesas=categorias["sobremesas"], bebidas=categorias["bebidas"],
                           is_admin=current_user.is_admin)

@app.route("/cardapio/adicionar", methods=["POST"])
@admin_required
def adicionar():
    produto = Produto(
        nome=request.form["nome"],
        preco=float(request.form["preco"]),
        imagem=request.form["url"],
        categoria=request.form["categoria"]
    )
    produto.save()
    flash("Produto adicionado com sucesso!", "success")
    return redirect(url_for("cardapio"))

@app.route("/cardapio/remover/<int:item>", methods=["POST"])
@admin_required
def remover(item):
    p = Produto.get(item)
    if p: p.delete()
    flash("Produto removido!", "success")
    return redirect(url_for("cardapio"))

@app.route("/cardapio/editar/<int:item>", methods=["POST"])
@admin_required
def editar(item):
    p = Produto.get(item)
    if p:
        p.update(nome=request.form["nome"], preco=float(request.form["preco"]),
                 url=request.form["url"], categoria=request.form["categoria"])
        flash("Produto editado!", "success")
    return redirect(url_for("cardapio"))

# ROTAS DE SACOLA
@app.route("/sacola")
@login_required
def ver_sacola():
    sacola = Sacola.get(current_user.id)
    itens = sacola.itens if sacola else []
    produtos_detalhes = []
    total = 0
    for i in itens:
        subtotal = i.produto.preco * i.quantidade
        total += subtotal
        produtos_detalhes.append({"item": i, "produto": i.produto, "subtotal": subtotal})
    return render_template("sacolas.html", itens=produtos_detalhes, total=total)

@app.route("/sacola/adicionar/<int:produto_id>", methods=["POST"])
@login_required
def adicionar_sacola(produto_id):
    quantidade = int(request.form.get("quantidade", 1))
    sacola = Sacola.get(current_user.id)
    if not sacola:
        sacola = Sacola(usuario_id=current_user.id)
        sacola.save()
    item = ItemSacola.query.filter_by(sacola_id=sacola.id, produto_id=produto_id).first()
    if item:
        item.atualizar_quantidade(item.quantidade + quantidade)
    else:
        ItemSacola(sacola_id=sacola.id, produto_id=produto_id, quantidade=quantidade).save()
    flash("Item adicionado!", "success")
    return redirect(url_for("ver_sacola"))

@app.route("/sacola/remover/<int:item_id>", methods=["POST"])
@login_required
def remover_sacola(item_id):
    item = ItemSacola.query.get(item_id)
    if item: item.delete()
    flash("Item removido!", "success")
    return redirect(url_for("ver_sacola"))

@app.route("/sacola/finalizar", methods=["POST"])
@login_required
def finalizar_sacola():
    sacola = Sacola.get(current_user.id)
    if not sacola or not sacola.itens:
        flash("Sacola vazia", "error")
        return redirect(url_for("cardapio"))

    total = sum(i.produto.preco * i.quantidade for i in sacola.itens)
    pedido = Pedido(usuario_id=current_user.id, total=total)
    pedido.save()
    for i in sacola.itens:
        ItemPedido(pedido_id=pedido.id, produto_id=i.produto_id, quantidade=i.quantidade).save()
    sacola.finalizar()
    flash("Compra finalizada!", "success")
    return redirect(url_for("cardapio"))

@app.route("/pedidos")
@login_required
def ver_pedidos():
    pedidos = Pedido.all(current_user.id)
    return render_template("pedidos.html", pedidos=pedidos)

# PERFIL
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.update(
            email=request.form["email"],
            senha=request.form["senha"],
            nome=request.form.get("nome"),
            cpf=request.form.get("cpf")
        )
        flash("Dados atualizados!", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", usuario=current_user, senha_visivel="******")

# ERROS
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("error/404.html"), 404

@app.errorhandler(500)
def erro_interno(error):
    return render_template("error/500.html"), 500

app.run(debug=True)
