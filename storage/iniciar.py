import sqlite3

BANCO='storage/schema.sql'

# conectar com o banco
conexao = sqlite3.connect('storage/banco.db')

# executar a criação tabela
with open(BANCO) as f:
    conexao.executescript(f.read())

conexao.close()
# fechar conexao

