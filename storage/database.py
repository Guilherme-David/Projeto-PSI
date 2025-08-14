import sqlite3

def obter_conexao():
    conexao = sqlite3.connect('storage/banco.db')
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao
