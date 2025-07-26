import sqlite3
from werkzeug.security import generate_password_hash

BANCO='storage/schema.sql'

# conectar com o banco
conexao = sqlite3.connect('storage/banco.db')

senha_admin =  generate_password_hash(input("Digite a senha do admin: "))

# executar a criação tabela
with open(BANCO) as f:
    conexao.executescript(f.read())

sql = "INSERT INTO tb_usuarios (usr_email, usr_senha, usr_is_admin) VALUES (?, ?, ?)"

conexao.execute(sql, ("admin@admin.com", senha_admin, True))
conexao.commit()
conexao.close()
# fechar conexao

