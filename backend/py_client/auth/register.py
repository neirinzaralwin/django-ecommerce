import requests
from getpass import getpass

endpoint = 'http://127.0.0.1:8000/api/register/'
username = input("What is your username to register?\n")
password = input("What is your password to register?\n")

data = {
        'username': username,
        'password': password
    }
response = requests.post(endpoint, json={'username': username,'password': password})

if response.status_code == 201:
    print(response.json())
    print(f'User: {username} created successfully.')
else:
    print(response.json())
    print(f'Failed to create user: {username}')