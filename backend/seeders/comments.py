import requests

BASE_URL = "http://127.0.0.1:8000/api"

comments = [
    {
        "commentId": 1,
        "task": 1,
        "body": "Estrutura inicial criada com sucesso.",
        "createdBy": 1
    },
    {
        "commentId": 2,
        "task": 1,
        "body": "Vou iniciar a implementação da autenticação.",
        "createdBy": 2
    },
    {
        "commentId": 3,
        "task": 2,
        "body": "JWT configurado corretamente.",
        "createdBy": 1
    },
    {
        "commentId": 4,
        "task": 3,
        "body": "Dashboard finalizado.",
        "createdBy": 2
    },
    {
        "commentId": 5,
        "task": 4,
        "body": "CRUD de usuários em andamento.",
        "createdBy": 3
    },
    {
        "commentId": 6,
        "task": 5,
        "body": "Documentação iniciada.",
        "createdBy": 3
    },
    {
        "commentId": 7,
        "task": 6,
        "body": "Conexão com MongoDB funcionando.",
        "createdBy": 1
    },
    {
        "commentId": 8,
        "task": 7,
        "body": "Endpoints de projetos implementados.",
        "createdBy": 2
    },
    {
        "commentId": 9,
        "task": 8,
        "body": "Relacionamento entre comentários e tarefas concluído.",
        "createdBy": 3
    },
    {
        "commentId": 10,
        "task": 9,
        "body": "Iniciando testes automatizados.",
        "createdBy": 1
    },
    {
        "commentId": 11,
        "task": 10,
        "body": "Deploy previsto para esta semana.",
        "createdBy": 2
    },
    {
        "commentId": 12,
        "task": 2,
        "body": "Realizada revisão do código.",
        "createdBy": 3
    },
    {
        "commentId": 13,
        "task": 4,
        "body": "Corrigidos alguns bugs encontrados.",
        "createdBy": 2
    },
    {
        "commentId": 14,
        "task": 6,
        "body": "Integração com PyMongo validada.",
        "createdBy": 1
    },
    {
        "commentId": 15,
        "task": 8,
        "body": "Comentários sendo exibidos corretamente no frontend.",
        "createdBy": 3
    }
]

for comment in comments:
    response = requests.post(f"{BASE_URL}/comments/", json=comment)

    print(f"Comentário {comment['commentId']}: {response.status_code}")

    try:
        print(response.json())
    except Exception:
        print(response.text)