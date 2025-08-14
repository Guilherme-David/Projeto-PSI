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
            return User(id=resultado['usr_id'],email=resultado['usr_email'], senha_hash=resultado['usr_senha'], is_admin=bool(resultado['usr_is_admin']),cpf=resultado["usr_cpf"],nome=resultado["usr_nome"])
        return None

    @classmethod
    def all(cls):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios"
        resultados = conexao.execute(sql, ).fetchall()
        conexao.close()
        usuarios = []
        for i in resultados:
            usuario = User(id=i['usr_id'],email=i['usr_email'], senha_hash=i['usr_senha'],is_admin=i['usr_is_admin'],cpf=["usr_cpf"],nome=["usr_nome"]  )
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
    def get(cls, produto_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_produtos WHERE pro_id = ?"
        resultado = conexao.execute(sql, (produto_id,)).fetchone()
        conexao.close()
        if resultado:
            return Produto(id=resultado['pro_id'], nome=resultado['pro_nome'], preco=float(resultado['pro_preco']), url_imagem=resultado['pro_url_imagem'], categoria=resultado['pro_categoria'])
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

    @classmethod
    def update(self, id, nome, preco, url, categoria):
        conexao = obter_conexao()
        sql = "UPDATE tb_produtos SET pro_nome = ?, pro_preco = ?, pro_url_imagem = ?, pro_categoria = ? WHERE pro_id = ?"
        conexao.execute(sql, (nome, preco, url, categoria, id))
        conexao.commit()
        conexao.close()
        self.nome = nome
        self.preco = preco
        self.imagem = url
        self.categoria = categoria

class Sacola:
    def __init__(self, id, usuario_id, status='ativa'):
        self.id = id
        self.usuario_id = usuario_id
        self.status = status

    @classmethod
    def get(cls, usuario_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_sacolas WHERE sac_usr_id = ? AND sac_status = 'ativa'"
        resultado = conexao.execute(sql, (usuario_id,)).fetchone()
        conexao.close()
        if resultado:
            return Sacola(id=resultado['sac_id'], usuario_id=resultado['sac_usr_id'], status=resultado['sac_status'])
        return None

    def save(self):
        conexao = obter_conexao()
        sql = "INSERT INTO tb_sacolas (sac_usr_id, sac_status) VALUES (?, ?)"
        cursor = conexao.execute(sql, (self.usuario_id, self.status))
        self.id = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return True

    def finalizar(self):
        conexao = obter_conexao()
        sql = "UPDATE tb_sacolas SET sac_status = 'finalizada' WHERE sac_id = ?"
        conexao.execute(sql, (self.id,))
        conexao.commit()
        conexao.close()
        self.status = 'finalizada'

class ItemSacola:
    def __init__(self, id, sacola_id, produto_id, quantidade):
        self.id = id
        self.sacola_id = sacola_id
        self.produto_id = produto_id
        self.quantidade = quantidade

    @classmethod
    def all(cls, sacola_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_itens_sacola WHERE itm_sac_id = ?"
        resultados = conexao.execute(sql, (sacola_id,)).fetchall()
        conexao.close()
        itens = []
        for i in resultados:
            itens.append(ItemSacola(id=i['itm_id'], sacola_id=i['itm_sac_id'], produto_id=i['itm_pro_id'], quantidade=i['itm_quantidade']))
        return itens

    def save(self):
        conexao = obter_conexao()
        sql = "INSERT INTO tb_itens_sacola (itm_sac_id, itm_pro_id, itm_quantidade) VALUES (?, ?, ?)"
        cursor = conexao.execute(sql, (self.sacola_id, self.produto_id, self.quantidade))
        self.id = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return True
    
    def atualizar_quantidade(self, nova_qtd):
        conexao = obter_conexao()
        sql = "UPDATE tb_itens_sacola SET itm_quantidade=? WHERE itm_id=?"
        conexao.execute(sql, (nova_qtd, self.id))
        conexao.commit()
        conexao.close()
        self.quantidade = nova_qtd

    @classmethod
    def delete(cls, item_id):
        conexao = obter_conexao()
        sql = "DELETE FROM tb_itens_sacola WHERE itm_id=?"
        conexao.execute(sql, (item_id,))
        conexao.commit()
        conexao.close()


class Pedido():
    def __init__(self, id, usuario_id, total):
        self.id = id
        self.usuario_id = usuario_id
        self.total = total

    def save(self):
        conexao = obter_conexao()
        sql = "INSERT INTO tb_pedidos (ped_usr_id, ped_total) VALUES (?, ?)"
        cursor = conexao.execute(sql, (self.usuario_id, self.total))
        self.id = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return True
    
    @classmethod
    def all(cls, usuario_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_pedidos WHERE ped_usr_id = ? ORDER BY ped_id DESC"
        resultados = conexao.execute(sql, (usuario_id,)).fetchall()
        conexao.close()

        pedidos = []
        for i in resultados:
            pedido = Pedido(id=i['ped_id'], usuario_id=i['ped_usr_id'],total=i['ped_total'])
            # Pega os itens do pedido
            itens = ItemPedido.all(pedido.id)
            # Para cada item, adiciona o produto completo
            for item in itens:
                item.produto = Produto.get(item.produto_id)
            pedido.itens = itens
            pedidos.append(pedido)
        return pedidos
        

class ItemPedido():
    def __init__(self, id, pedido_id, produto_id, quantidade):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade

    def save(self):
        conexao = obter_conexao()
        sql = "INSERT INTO tb_itens_pedido (itm_ped_id, itm_pro_id, itm_quantidade) VALUES (?, ?, ?)"
        cursor = conexao.execute(sql, (self.pedido_id, self.produto_id, self.quantidade))
        self.id = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return True
    
    @classmethod
    def all(cls, pedido_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_itens_pedido WHERE itm_ped_id = ?"
        resultados = conexao.execute(sql, (pedido_id,)).fetchall()
        conexao.close()
        itens = []
        for i in resultados:itens.append(ItemPedido(id=i['itm_id'],pedido_id=i['itm_ped_id'],produto_id=i['itm_pro_id'],quantidade=i['itm_quantidade']))
        return itens