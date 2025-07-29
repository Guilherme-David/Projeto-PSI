from flask_login import UserMixin
from storage.database import obter_conexao
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self, id, email, senha_hash, is_admin = False, nome=None, cpf=None):
        self.id = id
        self.email = email
        self.senha_hash = senha_hash
        self.is_admin = is_admin
        self.nome = nome
        self.cpf = cpf

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios WHERE usr_id = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()
        if resultado:
            return User(id=resultado['usr_id'],email=resultado['usr_email'], senha_hash=resultado['usr_senha'], is_admin=bool(resultado['usr_is_admin']))
        return None

    @classmethod
    def all(cls):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios"
        resultados = conexao.execute(sql, ).fetchall()
        conexao.close()
        usuarios = []
        for i in resultados:
            usuario = User(id=i['usr_id'],email=i['usr_email'], senha_hash=i['usr_senha'],is_admin=i['usr_is_admin']  )
            usuarios.append(usuario)
        return usuarios

    def save(self):
        conexao = obter_conexao()

        # Verifica se usuário já existe
        sql = "SELECT * FROM tb_usuarios WHERE usr_email = ?"
        resultado = conexao.execute(sql, (self.email,)).fetchone()
        if resultado:
            conexao.close()
            return None
        else:
            # Insere novo usuário
            sql_insert = "INSERT INTO tb_usuarios (usr_email, usr_senha, usr_is_admin) VALUES (?, ?, ?)"
            cursor = conexao.execute(sql_insert, (self.email, self.senha_hash, int(self.is_admin)))
            self.id = cursor.lastrowid
            conexao.commit()
            conexao.close()
            return True

    @classmethod
    def delete(cls, email):
        conexao = obter_conexao()

        sql = "DELETE FROM tb_usuarios WHERE usr_email = ?"
        conexao.execute(sql, (email,))
        conexao.commit()
        conexao.close()
    
    def update(self, email, senha, nome, cpf): #nao chequei tudo dessa função
        conexao = obter_conexao()
        senha_hash = generate_password_hash(senha) #hash para a senha nova
        sql = "UPDATE tb_usuarios SET usr_email = ?, usr_senha = ?, usr_nome = ?, usr_cpf = ? WHERE usr_id = ?"
        conexao.execute(sql, (email, senha_hash, nome, cpf, self.id))
        conexao.commit()
        conexao.close()
        #atualiza os atributos do objeto pra ficar de igual com os dados novos
        self.email = email
        self.senha_hash = senha_hash
        self.nome = nome
        self.cpf = cpf

class Produto():
    def __init__(self, id, nome, preco, url_imagem, categoria):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.imagem = url_imagem
        self.categoria = categoria

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_produtos WHERE pro_id = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()
        if resultado:
            return Produto(id=['pro_id'], nome=['pro_nome'], preco=['pro_preco'], imagem=['pro_url_imagem'], categoria=['pro_categoria'])
        return None


    @classmethod
    def all(cls):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_produtos"
        resultados = conexao.execute(sql, ).fetchall()
        conexao.close()
        produtos = []
        for i in resultados:
            produto = Produto(id=i['pro_id'], nome=i['pro_nome'], preco=i['pro_preco'], url_imagem=i['pro_url_imagem'], categoria=i['pro_categoria'])
            produtos.append(produto)
        return produtos

    def save(self):
        conexao = obter_conexao()

        # Insere novo produto
        sql_insert = "INSERT INTO tb_produtos (pro_nome, pro_preco, pro_url_imagem, pro_categoria) VALUES (?, ?, ?, ?)"
        conexao.execute(sql_insert, (self.nome, self.preco, self.imagem, self.categoria))
        conexao.commit()
        conexao.close()
        return True

    @classmethod
    def delete(cls, id):
        conexao = obter_conexao()
        sql = "DELETE FROM tb_produtos WHERE pro_id = ?"
        conexao.execute(sql, (id,))
        conexao.commit()
        conexao.close()