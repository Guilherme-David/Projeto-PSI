from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# ---------------------- USUÁRIO ----------------------
class User(UserMixin, db.Model):
    __tablename__ = "tb_usuarios"

    id = db.Column("usr_id", db.Integer, primary_key=True)
    email = db.Column("usr_email", db.String(150), unique=True, nullable=False)
    senha_hash = db.Column("usr_senha", db.String(200), nullable=False)
    is_admin = db.Column("usr_is_admin", db.Boolean, default=False)
    nome = db.Column("usr_nome", db.String(150))
    cpf = db.Column("usr_cpf", db.String(14))

    @classmethod
    def get(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    def update(self, email=None, senha=None, nome=None, cpf=None):
        if email:
            self.email = email
        if senha:
            self.senha_hash = generate_password_hash(senha)
        if nome:
            self.nome = nome
        if cpf:
            self.cpf = cpf
        db.session.commit()
        return self

    @classmethod
    def delete_by_email(cls, email):
        u = cls.query.filter_by(email=email).first()
        if u:
            db.session.delete(u)
            db.session.commit()
            return True
        return False


# ---------------------- PRODUTO ----------------------
class Produto(db.Model):
    __tablename__ = "tb_produtos"

    id = db.Column("pro_id", db.Integer, primary_key=True)
    nome = db.Column("pro_nome", db.String(255), nullable=False)
    preco = db.Column("pro_preco", db.Float, nullable=False)
    imagem = db.Column("pro_url_imagem", db.String(255))
    categoria = db.Column("pro_categoria", db.String(50))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    def update(self, nome=None, preco=None, url=None, categoria=None):
        if nome:
            self.nome = nome
        if preco:
            self.preco = preco
        if url:
            self.imagem = url
        if categoria:
            self.categoria = categoria
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# ---------------------- SACOLA ----------------------
class Sacola(db.Model):
    __tablename__ = "tb_sacolas"

    id = db.Column("sac_id", db.Integer, primary_key=True)
    usuario_id = db.Column("sac_usr_id", db.Integer, db.ForeignKey("tb_usuarios.usr_id"))
    status = db.Column("sac_status", db.String(20), default="ativa")

    itens = db.relationship("ItemSacola", backref="sacola", lazy=True)

    @classmethod
    def get(cls, usuario_id):
        return cls.query.filter_by(usuario_id=usuario_id, status="ativa").first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    def finalizar(self):
        self.status = "finalizada"
        db.session.commit()
        return self


# ---------------------- ITEM SACOLA ----------------------
class ItemSacola(db.Model):
    __tablename__ = "tb_itens_sacola"

    id = db.Column("itm_id", db.Integer, primary_key=True)
    sacola_id = db.Column("itm_sac_id", db.Integer, db.ForeignKey("tb_sacolas.sac_id"))
    produto_id = db.Column("itm_pro_id", db.Integer, db.ForeignKey("tb_produtos.pro_id"))
    quantidade = db.Column("itm_quantidade", db.Integer, default=1)

    produto = db.relationship("Produto", backref="itens_sacola", lazy=True)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    def atualizar_quantidade(self, nova_qtd):
        self.quantidade = nova_qtd
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls, sacola_id):
        return cls.query.filter_by(sacola_id=sacola_id).all()

# ---------------------- PEDIDO ----------------------
class Pedido(db.Model):
    __tablename__ = "tb_pedidos"

    id = db.Column("ped_id", db.Integer, primary_key=True)
    usuario_id = db.Column("ped_usr_id", db.Integer, db.ForeignKey("tb_usuarios.usr_id"))
    total = db.Column("ped_total", db.Float)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls, usuario_id):
        return cls.query.filter_by(usuario_id=usuario_id).order_by(cls.id.desc()).all()


# ---------------------- ITEM PEDIDO ----------------------
class ItemPedido(db.Model):
    __tablename__ = "tb_itens_pedido"

    id = db.Column("itm_id", db.Integer, primary_key=True)
    pedido_id = db.Column("itm_ped_id", db.Integer, db.ForeignKey("tb_pedidos.ped_id"))
    produto_id = db.Column("itm_pro_id", db.Integer, db.ForeignKey("tb_produtos.pro_id"))
    quantidade = db.Column("itm_quantidade", db.Integer)

    produto = db.relationship("Produto", backref="itens_pedido", lazy=True)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls, pedido_id):
        return cls.query.filter_by(pedido_id=pedido_id).all()
