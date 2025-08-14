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
    pro_url_imagem TEXT NOT NULL,
    pro_categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_sacolas (
    sac_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sac_usr_id INTEGER NOT NULL,
    sac_status TEXT CHECK(sac_status IN ('ativa','finalizada')) DEFAULT 'ativa',
    FOREIGN KEY(sac_usr_id) REFERENCES tb_usuarios(usr_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_itens_sacola (
    itm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    itm_sac_id INTEGER NOT NULL,
    itm_pro_id INTEGER NOT NULL,
    itm_quantidade INTEGER NOT NULL,
    FOREIGN KEY(itm_sac_id) REFERENCES tb_sacolas(sac_id) ON DELETE CASCADE,
    FOREIGN KEY(itm_pro_id) REFERENCES tb_produtos(pro_id)
);

CREATE TABLE IF NOT EXISTS tb_pedidos (
    ped_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ped_usr_id INTEGER NOT NULL,
    ped_total REAL NOT NULL DEFAULT 0,
    FOREIGN KEY(ped_usr_id) REFERENCES tb_usuarios(usr_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_itens_pedido (
    itm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    itm_ped_id INTEGER NOT NULL,
    itm_pro_id INTEGER NOT NULL,
    itm_quantidade INTEGER NOT NULL,
    FOREIGN KEY(itm_ped_id) REFERENCES tb_pedidos(ped_id) ON DELETE CASCADE,
    FOREIGN KEY(itm_pro_id) REFERENCES tb_produtos(pro_id)
);
