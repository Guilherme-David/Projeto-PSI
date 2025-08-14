from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import secrets
from storage.database import obter_conexao
from models import User, Produto, Sacola, ItemSacola, Pedido, ItemPedido
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import admin_required

secret_key = secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.context_processor
def compartilhar_autenticado(): #Decorator com função que compartilha a informação do estado do usuário (logado ou não logado), para a personalização da navbar
    return {"is_authenticated": current_user.is_authenticated}

@app.route('/', methods = ["GET", "POST"])
def home():
    return render_template("index.html")

# ---------------------- ROTAS DE AUTENTICAÇÃO ----------------------
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        senha= request.form['senha']
        senha_hash = generate_password_hash(senha)
        user = User(id=None, email=email, senha_hash=senha_hash)
        sucesso = user.save()
        if sucesso:
            login_user(user)
            return redirect(url_for('cardapio'))
        else:
            flash("E-mail já cadastrado.", "error")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha= request.form['senha']

        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios WHERE usr_email = ?"
        resultado = conexao.execute(sql, (email,)).fetchone()
        conexao.close()

        if resultado and check_password_hash(resultado['usr_senha'], senha):
            user = User(id=resultado['usr_id'],email=resultado['usr_email'],senha_hash=resultado['usr_senha'],is_admin=bool(resultado['usr_is_admin']))
            login_user(user)
            return redirect(url_for('cardapio'))
        else:
            flash("Usuário ou senha incorretos. Tente novamente.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ---------------------- ROTAS DE PRODUTOS ----------------------
@app.route("/cardapio", methods = ["GET"])
@login_required
def cardapio():
    produtos = Produto.all() 
    is_admin = bool(current_user.is_admin)
    hamburguers = []
    sobremesas = []
    bebidas = []
    for produto in produtos:
        if produto.categoria == 'sobremesas':
            sobremesas.append(produto)
        elif produto.categoria == 'hamburguers':
            hamburguers.append(produto)
        elif produto.categoria == 'bebidas':
            bebidas.append(produto)
    return render_template("produtos.html", hamburguers=hamburguers, bebidas=bebidas, sobremesas=sobremesas, is_admin=is_admin)

@app.route('/cardapio/adicionar', methods = ["POST"])
@admin_required
def adicionar():
    nome_produto = request.form['nome']
    preco = request.form['preco']
    url_imagem = request.form['url']
    categoria = request.form['categoria']
    produto = Produto(id=None, nome=nome_produto, preco=preco, url_imagem=url_imagem, categoria=categoria)
    produto.save()
    flash("Produto adicionado com sucesso!", "success")
    return redirect(url_for('cardapio'))

@app.route('/cardapio/remover/<item>', methods=["POST"])
@admin_required
def remover(item):
    Produto.delete(item)
    flash("Produto removido com sucesso!", "success")
    return redirect(url_for('cardapio'))

@app.route('/cardapio/editar/<item>', methods=["POST"])
@admin_required
def editar(item):

    novo_nome_produto = request.form['nome']
    novo_preco = request.form['preco']
    nova_url_imagem = request.form['url']
    nova_categoria = request.form['categoria']

    Produto.update(item, novo_nome_produto, novo_preco, nova_url_imagem, nova_categoria)
    flash("Produto editado com sucesso!", "success")
    return redirect(url_for('cardapio'))

# ---------------------- ROTAS DE SACOLA/PEDIDOS ----------------------
@app.route('/sacola', methods=["GET"])
@login_required
def ver_sacola():
    sacola = Sacola.get(current_user.id)
    if sacola:
        itens = ItemSacola.all(sacola.id) 
    else: 
        itens = []
    produtos_detalhes = []
    total = 0
    for item in itens:
        produto = Produto.get(item.produto_id)
        subtotal = produto.preco * item.quantidade
        total += subtotal
        produtos_detalhes.append({'item': item, 'produto': produto, 'subtotal': subtotal})
    return render_template('sacolas.html', itens=produtos_detalhes, total=total)

@app.route('/sacola/adicionar/<produto_id>', methods=["POST"])
@login_required
def adicionar_sacola(produto_id):
    quantidade = int(request.form.get('quantidade', 1))
    sacola = Sacola.get(current_user.id)
    if not sacola:
        sacola = Sacola(id=None, usuario_id=current_user.id)
        sacola.save()
    # Verifica se item já existe
    itens = ItemSacola.all(sacola.id)
    for item in itens:
        if item.produto_id == int(produto_id):
            item.atualizar_quantidade(item.quantidade + quantidade)
            break
    else:
        novo_item = ItemSacola(id=None, sacola_id=sacola.id, produto_id=produto_id, quantidade=quantidade)
        novo_item.save()
    flash("Item adicionado à sacola", "success")
    return redirect(url_for('ver_sacola'))

@app.route('/sacola/remover/<item_id>', methods=["POST"])
@login_required
def remover_sacola(item_id):
    ItemSacola.delete(item_id)
    flash("Item removido da sacola", "success")
    return redirect(url_for('ver_sacola'))

@app.route('/sacola/finalizar', methods=["POST"])
@login_required
def finalizar_sacola():
    sacola = Sacola.get(current_user.id)
    if not sacola:
        flash("Sacola vazia", "error")
        return redirect(url_for('cardapio'))
    itens = ItemSacola.all(sacola.id)
    total = 0
    for item in itens:
        total += Produto.get(item.produto_id).preco * item.quantidade
    pedido = Pedido(id=None, usuario_id=current_user.id, total=total)
    pedido.save()
    # Copia itens da sacola para o pedido
    for item in itens:
        produto = Produto.get(item.produto_id)
        ip = ItemPedido(id=None, pedido_id=pedido.id, produto_id=produto.id,quantidade=item.quantidade)
        ip.save()
    # Finaliza a sacola
    sacola.finalizar()
    flash("Compra finalizada com sucesso", "success")
    return redirect(url_for('cardapio'))

@app.route("/pedidos")
@login_required
def ver_pedidos():
    pedidos = Pedido.all(current_user.id)
    return render_template("pedidos.html", pedidos=pedidos)

# ---------------------- PERFIL ----------------------
@app.route("/profile", methods = ["GET", "POST"])
@login_required
def profile():
    if request.method == 'POST':
        novo_email = request.form['email']
        nova_senha = request.form['senha']
        nome = request.form.get('nome', None)
        cpf = request.form.get('cpf', None)

        #atualiza os dados do usuario q ta logado na pagina com os valores novos n testei ainda com o nome e cpf
        current_user.update(novo_email, nova_senha, nome, cpf)
        flash("dados mudados com suceso", "success") #msg de teste pra saber se deu certo
        return redirect(url_for('profile'))
    
    senha_visivel = "******" #valor inutil pra n exibir a senha original logo de cara, ai pra ver prescisa apertar no botao
    return render_template("profile.html", usuario=current_user, senha_visivel=senha_visivel)

# ---------------------- ERROS ----------------------
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("error/404.html"), 404

@app.route('/erro500') #pag de teste de erro 500
def erro500():
    # erro
    return 1 / 0

@app.errorhandler(500)
def erro_interno(error):
    return render_template("error/500.html"), 500