# FDG Burguer

Sistema web para gerenciamento e vendas da lanchonete FDG Burguer.  
Possui funcionalidades como cadastro/login de usuários, listagem de produtos, gerenciamento de pedidos e página de perfil.

---

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`.  
Principais bibliotecas:

- **Flask** — Framework web em Python.
- **Flask-Login** — Gerenciamento de autenticação de usuários.
- **SQLite** — Banco de dados local.
- **Werkzeug** — Utilitários para segurança e autenticação.
- Outras dependências listadas no arquivo `requirements.txt`.

---

## Instruções para rodar localmente

1. **Clonar ou extrair o projeto**
    ```bash
    git clone https://github.com/Guilherme-David/Projeto-PSI.git
    cd <pasta onde foi feito a clonagem>

2. **Criar e ativar um ambiente virtual (opcional)**
    # Windows
    ```bash
        python -m venv venv.
        venv\Scripts\activate
3. **Instalar As dependencias**
    ```bash
    pip install -r requirements.txt
4. **Inicializar o banco de dados**
    Caso o banco não exista, rode:
    ```bash
    python storage/iniciar.py
5. **Executar a aplicação**
    ```bash
    python app.py
6. **Acesse No Navegador**
    ```bash
    http://127.0.0.1:5000
## 🗒️ Observações

- O banco de dados padrão (storage/banco.db) já pode vir pré-criado.

- Caso queira começar do zero, delete o arquivo banco.db e rode python storage/iniciar.py.

- Certifique-se de estar usando Python 3.10+ para compatibilidade.

- Caso queira testar a pagina de Erro500 certifique-se de não estar debugando o flask.

## Estutura Do Projeto
    ├── app.py                  # Arquivo principal da aplicação Flask
    ├── requirements.txt        # Dependências do projeto
    ├── models/                 # Modelos e lógica de negócios
    ├── static/                 # Arquivos estáticos (CSS, imagens)
    ├── templates/              # Templates HTML (Jinja2)
    ├── storage/                # Banco de dados e scripts de inicialização
    └── .gitignore