import requests
from getpass import getpass

endpoint = 'http://127.0.0.1:8000/api/register/'
name = input("What is your name to register?\n")
email = input("What is your email to register?\n")
password = input("What is your password to register?\n")

data = {
        'name': name,
        'email': email,
        'password': password
    }
response = requests.post(endpoint, json=data)

if response.status_code == 201:
    print(response.json())
    print(f'User: {username} created successfully.')
else:
    print(response.json())
    print(f'Failed to create user: {username}')