import requests

BASE_URL = "http://127.0.0.1:8000/api"

tasks = [
    {
        "taskId": 1,
        "project": 1,
        "title": "Criar estrutura do projeto",
        "description": "Configurar Django REST Framework",
        "createdBy": 1,
        "priority": "high",
        "done": False,
        "startDate": "2026-07-01T09:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 2,
        "project": 1,
        "title": "Implementar autenticação",
        "description": "Criar sistema de login",
        "createdBy": 2,
        "priority": "high",
        "done": False,
        "startDate": "2026-07-02T10:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 3,
        "project": 2,
        "title": "Criar tela inicial",
        "description": "Desenvolver dashboard",
        "createdBy": 2,
        "priority": "medium",
        "done": True,
        "startDate": "2026-07-01T08:00:00Z",
        "completedAt": "2026-07-03T15:30:00Z",
        "completedBy": 2
    },
    {
        "taskId": 4,
        "project": 2,
        "title": "Cadastrar usuários",
        "description": "Criar CRUD de usuários",
        "createdBy": 3,
        "priority": "medium",
        "done": False,
        "startDate": "2026-07-04T13:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 5,
        "project": 3,
        "title": "Criar documentação",
        "description": "Documentar endpoints da API",
        "createdBy": 3,
        "priority": "low",
        "done": False,
        "startDate": "2026-07-05T14:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 6,
        "project": 4,
        "title": "Implementar MongoDB",
        "description": "Conectar aplicação ao banco",
        "createdBy": 1,
        "priority": "high",
        "done": True,
        "startDate": "2026-07-02T09:30:00Z",
        "completedAt": "2026-07-02T18:00:00Z",
        "completedBy": 1
    },
    {
        "taskId": 7,
        "project": 4,
        "title": "Criar API de projetos",
        "description": "Endpoints CRUD",
        "createdBy": 2,
        "priority": "medium",
        "done": False,
        "startDate": "2026-07-06T10:30:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 8,
        "project": 5,
        "title": "Implementar comentários",
        "description": "Relacionar comentários às tarefas",
        "createdBy": 3,
        "priority": "low",
        "done": False,
        "startDate": "2026-07-07T11:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 9,
        "project": 5,
        "title": "Criar testes",
        "description": "Testar endpoints da API",
        "createdBy": 1,
        "priority": "high",
        "done": False,
        "startDate": "2026-07-08T09:00:00Z",
        "completedAt": None,
        "completedBy": None
    },
    {
        "taskId": 10,
        "project": 3,
        "title": "Deploy da aplicação",
        "description": "Publicar API em produção",
        "createdBy": 2,
        "priority": "high",
        "done": False,
        "startDate": "2026-07-09T16:00:00Z",
        "completedAt": None,
        "completedBy": None
    }
]

for task in tasks:
    response = requests.post(f"{BASE_URL}/tasks/", json=task)

    print(f"Tarefa {task['taskId']}: {response.status_code}")

    try:
        print(response.json())
    except Exception:
        print(response.text)