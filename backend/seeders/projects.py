import requests

BASE_URL = "http://127.0.0.1:8000/api"

projects = [
    {
        "projectId": 1,
        "name": "API REST MongoDB",
        "description": "Projeto para estudo de Django REST Framework com PyMongo",
        "owner": 1,
        "members": [1, 2, 3]
    },
    {
        "projectId": 2,
        "name": "Sistema de Gerenciamento de Tarefas",
        "description": "Aplicação para gerenciamento de tarefas em equipe",
        "owner": 2,
        "members": [2, 3]
    },
    {
        "projectId": 3,
        "name": "Portal Acadêmico",
        "description": "Sistema para gerenciamento de documentos acadêmicos",
        "owner": 3,
        "members": [1, 3]
    },
    {
        "projectId": 4,
        "name": "E-commerce",
        "description": "Loja virtual desenvolvida em Django",
        "owner": 1,
        "members": [1, 2]
    },
    {
        "projectId": 5,
        "name": "Aplicativo Mobile",
        "description": "Backend para aplicativo de gerenciamento financeiro",
        "owner": 2,
        "members": [1, 2, 3]
    }
]

for project in projects:
    r = requests.post(f"{BASE_URL}/projects/", json=project)

    print(f"Projeto {project['projectId']}: {r.status_code}")

    try:
        print(r.json())
    except Exception:
        print(r.text)