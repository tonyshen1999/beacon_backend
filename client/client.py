import requests

endpoint = "http://127.0.0.1:8000/calc/"

response = requests.post(endpoint)

print(requests.get("http://127.0.0.1:8000/acc/").json())