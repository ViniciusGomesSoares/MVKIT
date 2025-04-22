# 🚀 Projeto - MVKIT
Este projeto é um sistema Web desenvolvido com **Python** , **HTML** e **CSS** permitindo o gerenciamento de restaurantes, produtos, carrinho de compras e um sistema de cadastro baseado no IFOOD

---

## 📋 Pré-requisitos
Antes de começar, você precisa ter instalado no seu sistema:
- **Instale o** **[Python]( https://www.python.org/downloads/)**
- **Um editor de código**, como **[VS Code](https://code.visualstudio.com/)**
- Para armazenas as informações no banco de dados instale o **[MongoDB](https://www.mongodb.com/products/tools/compass)**
- **[Git](https://git-scm.com/)** (opcional, mas recomendado)

---

## 🔧 Como rodar o projeto?

### 1️⃣ Clone o repositório:
Abra o terminal (cmd, PowerShell ou Git Bash) e execute:
```sh
git clone https://github.com/seu-usuario/meu-projeto.git
cd meu-projeto
```
### 2️⃣ Crie e ative um ambiente virtual (recomendado):
Usar uma venv garante que as dependências do projeto não interfiram em outros projetos ou no sistema.

#### 🐍 No Windows:
```sh
python -m venv venv
venv\Scripts\activate
```
#### 🐧 No macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```
Após ativar a venv, você verá algo parecido com (venv) no início da linha do terminal.

### 3️⃣ Instale as dependências:
```sh
pip install -r requirements.txt
```

---

## 🔹 Observações
O projeto utiliza:

- **Python** para fazer o gerenciamentos de rotas
- **HTML** para a interface
- **CSS** para estilização
- **BootStrap** para interface e estilazação
- **Tailwind** para interface e estilazação
- **MongoDB** para o Banco de dados

Caso ocorra erro ao executar o `.exe`, verifique se os arquivos de build foram gerados corretamente e se os caminhos dos arquivos estão corretos no `main.js`.
```sh
📦 MeuProjeto  
├── 📂 static             # Arquivos estáticos (CSS, JS, imagens, etc.)
├── 📂 templates          # Templates HTML do projeto
├── .gitignore            # Arquivos/pastas ignorados pelo Git  
├── app.py                # Arquivo principal da aplicação Flask  
├── authy.py              # Lógica de autenticação  
├── cadastro.py           # Lógica de cadastro de usuários  
├── cadrestaurante.py     # Lógica de cadastro de restaurantes  
├── endereco.py           # Gerenciamento de endereços  
├── requirements.txt      # Lista de dependências do projeto  
└── routes.py             # Definição das rotas da aplicação  
```

### 🙌 Agradecimentos
Este projeto foi idealizado e desenvolvido com dedicação pelo grupo MVKIT, formado por mentes brilhantes e apaixonadas por tecnologia:

💡 Vinícius Gomes Soares

💡 Kauê Oliveira Costa

💡 Thiago felix silva

💡 Matheus Geraldi da Silva

💡 Igor Isidoro de Souza

"Juntos, transformamos ideias em código e código em soluções." 🚀

Feito com 💙 por MVKIT
