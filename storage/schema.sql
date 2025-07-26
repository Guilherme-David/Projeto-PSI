create table if not exists tb_usuarios (
    usr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usr_email TEXT NOT NULL UNIQUE,
    usr_senha TEXT NOT NULL,
    usr_is_admin BOOLEAN NOT NULL DEFAULT 0
);

ALTER TABLE tb_usuarios ADD COLUMN usr_nome TEXT;
ALTER TABLE tb_usuarios ADD COLUMN usr_cpf TEXT;

CREATE TABLE if not exists tb_produtos (
    pro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pro_nome TEXT NOT NULL,
    pro_preco TEXT NOT NULL,
    pro_url_imagem TEXT NOT NULL 
);