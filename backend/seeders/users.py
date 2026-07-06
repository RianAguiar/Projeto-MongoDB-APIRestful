import requests

BASE_URL = "http://127.0.0.1:8000/api"

users = [
    {
        "userId": 1,
        "name": "João Silva",
        "username": "joao",
        "email": "joao@email.com",
        "password": "123456",
        "role": "admin"
    },
    {
        "userId": 2,
        "name": "Maria",
        "username": "maria",
        "email": "maria@email.com",
        "password": "123456",
        "role": "member"
    }
]

for user in users:
    r = requests.post(f"{BASE_URL}/users/", json=user)
    print(r.status_code, r.json())