from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
import secrets
import sqlite3
from storage.database import obter_conexao
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

secret_key = secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
        salvar = user.save()
        login_user(user)
        return redirect(url_for('produtos'))
            
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha= request.form['senha']

        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios WHERE email = ?"
        resultado = conexao.execute(sql, (email,)).fetchone()

        if resultado and check_password_hash(resultado['senha'], senha):
            user = User(id=resultado['id'],email=resultado['email'],senha_hash=resultado['senha'],is_admin=bool(resultado['is_admin']))
            login_user(user)
            return redirect(url_for('produtos'))
        return redirect(url_for('login'))
    return render_template('login.html')
    
@app.route("/produtos", methods = ["GET", "POST"])
@login_required
def produtos():
    return render_template("produtos.html")

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))