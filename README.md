# Sheuze Bux E-commerce Store

Este é um projeto de loja de e-commerce full-stack construído com Python e Django.

## Como Iniciar

Siga estas instruções para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

- Python 3.8 ou superior
- Pip

### 2. Configuração do Ambiente

Primeiro, clone o repositório e navegue até o diretório do projeto. Em seguida, crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Agora, instale todas as dependências necessárias usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

Aplique as migrações do banco de dados para criar as tabelas necessárias:

```bash
python manage.py migrate
```

Crie um superusuário para acessar o painel de administração do Django:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir um nome de usuário, e-mail e senha.

### 4. Configuração do Bot do Discord

O bot do Discord usa variáveis de ambiente para o token e o ID do canal. Você precisará criá-las antes de executar o bot.

Exporte as seguintes variáveis de ambiente em seu terminal:

```bash
export DISCORD_TOKEN="SEU_TOKEN_AQUI"
export DISCORD_CHANNEL_ID="SEU_ID_DE_CANAL_AQUI"
```

**Importante:** Substitua `"SEU_TOKEN_AQUI"` e `"SEU_ID_DE_CANAL_AQUI"` com suas credenciais reais.

### 5. Executando os Servidores

Você precisará de dois terminais abertos para executar a aplicação completa.

**Terminal 1: Servidor Web Django**

Inicie o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

A loja estará acessível em `http://127.0.0.1:8000`.

**Terminal 2: Bot do Discord**

No segundo terminal (com as variáveis de ambiente exportadas), inicie o bot do Discord:

```bash
python discord_bot.py
```

O bot ficará online e começará a monitorar os pagamentos pendentes.

### Acesso ao Painel de Administração

Para adicionar produtos e gerenciar pedidos, acesse o painel de administração em `http://127.0.0.1:8000/admin` e faça login com as credenciais de superusuário que você criou.
