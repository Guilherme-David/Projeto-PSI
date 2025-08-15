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
    venv\Scripts\activate
    flask run --debug
6. **Acesse No Navegador**
    ```bash
    http://127.0.0.1:5000

##  Funcionalidades

- O sistema possui autenticação(cadastro e login) usando flask-login.

- Existe um usuário admin cujo no banco de dados pré-criado seu email é admin@admin.com e a senha é 123.

- O usuário admin tem funcionalidades especiais, como a de cadastar, editar e deletar produtos do cardápio.

- A rota profile permite a alteração de dados do usuário

- O sistema possui a rota "/cardapio" que permite visualizar os produtos da hamburgueria

- Como usuário comum, não utilizando um usuário administrador, em cada produto você pode definir uma quantidade que quiser e adicioná-lo à sacola

- O sistema possui a rota "/sacola", nela você pode ver detalhes do pedido e finalizar a compra caso já tenha colocado os itens desejados, 
 caso contrário, retorne a rota do cardápio e adicione novos itens(individualmente).

- O sistema possui a rota "/pedidos" onde você pode ver seu histórico de pedidos.


## 🗒️ Observações (!IMPORTANTE!)

- O banco de dados padrão (storage/banco.db) já pode vir pré-criado.

- Caso queira começar do zero, delete o arquivo banco.db e rode python storage/iniciar.py. Porém, recomendamos que use o banco que já estará implementado pois já tem dados de teste dentro.

- Certifique-se de estar usando Python 3.10+ para compatibilidade.

- Caso queira testar a pagina de Erro500 certifique-se de não estar debugando o flask. Use "flask run", e não "flask run --debug". Para acessá-la, use a rota "/erro550".

## 🗒️ Contribuições 
   - O grupo é composto pelos alunos: David Gabriel, Fabian Messy, Guilherme David e Kaik Emanuel.
   - O aluno David Gabriel criou as seguintes rotas e seus respectivos templates: "Cardápio", "Sacola", "Pedidos". Além disso, fez todo o CRUD de usuários, produtos, sacolas e pedidos presentes no arquivo             __init.py__ presente no diretório models.
   - O aluno Fabian Messy criou as seguintes rotas e seus respectivos templates: "Index", "Profile". Além disso, ajudou na correção de bugs do código, contribuiu na implementação do CRUD de usuários, produtos,        sacolas e pedidos, implementou diversos scripts de JS e ajudou na estilização(css) das páginas  do projeto.
   - O aluno Guilherme David criou as seguintes rotas e seus respectivos templates: "Login", "Register". contribuiu na correção de bugs pelo código e na criação da estrutura que sustenta o banco de dados.
   - O aluno Kaik Emanuel ajudou na estilização geral do projeto(css), contribuiu com a implementação das mensagens flash. Por fim, contribuiu na correção de bugs pelo código.

## Estutura Do Projeto
    ├── app.py                  # Arquivo principal da aplicação Flask
    ├── requirements.txt        # Dependências do projeto
    ├── models/                 # Modelos e lógica de negócios
    ├── static/                 # Arquivos estáticos (CSS, imagens)
    ├── templates/              # Templates HTML (Jinja2)
    ├── storage/                # Banco de dados e scripts de inicialização
    ├── decorators/             # Decoradores especiais para controlar acesso
    └── .gitignore
