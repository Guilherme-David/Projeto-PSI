from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import secrets
from storage.database import obter_conexao
from models import User, Produto
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
            # flash("E-mail já cadastrado.") MENSAGEM DE ERRO, ADICIONAR DEPOIS
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
        return redirect(url_for('login'))
    return render_template('login.html')
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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
    #MENSAGEM DE PRODUTO CADASTRADO
    return redirect(url_for('cardapio'))

@app.route('/cardapio/remover/<item>', methods=["POST"])
@admin_required
def remover(item):
    Produto.delete(item)
    return redirect(url_for('cardapio'))

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

    