# Projeto MongoDB APIRestful

API REST Django REST Framework e MongoDB (Projeto Faculdade)
Utilizamos MongoDB com PyMongo sem ORM do Django

## Features
- Cadastro de usuários
- Gerenciamento de projetos e tarefas
- Sistema de comentários

## Antes de tudo
instale:

- MongoDB Community Server
- MongoDB Compass (opcional)

## Instalação

### 1. Clone o repositório

```bash
git clone <https://github.com/RianAguiar/Projeto-MongoDB-APIRestful>
```

### 2. Crie um ambiente virtual

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```


### 4. Inicie o serviço do MongoDB

inicie o serviço pelo painel **Serviços** do Windows

### 5. MongoDB Compass (Opcional)

Abra o MongoDB Compass e conecte utilizando:

```
mongodb://localhost:27017/
```

Coloque o nome da conexão de `database.py`.

## Executando a aplicação

Entre na pasta do backend:

```bash
cd backend
```

Execute o servidor:

```bash
python manage.py runserver
```

No browser entre em:

```
http://127.0.0.1:8000/
```

## Inserindo infos no banco de dados

Execute os seeders nessa ordem:

```bash
python seeders/users.py
python seeders/projects.py
python seeders/tasks.py
python seeders/comments.py
```

Execute nessa ordem por conta das dependências

## Fluxo de requisição geral

Cliente (React, Postman, App)
            │
            │ HTTP Request
            ▼
      URL / Endpoint
            │
            ▼
         urls.py
            │
            ▼
      View (APIView)
            │
            ▼
      Repository
 (operações no MongoDB)            
            │
            ▼
        MongoDB
            │
            ▼
      View (APIView)
            │
            ▼
      Serializer
 (valida os dados recebidos e converte)
            │
            ▼
 HTTP Response
            │
            ▼
Cliente.
