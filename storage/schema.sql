create table if not exists tb_usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

ALTER TABLE tb_usuarios ADD COLUMN nome TEXT;
ALTER TABLE tb_usuarios ADD COLUMN cpf TEXT;