import requests

endpoint = "http://127.0.0.1:8000/adj/"
data = {
    "account":1,
    "adj_type":"M-1",
    "adj_amount":10
}
# requests.post(endpoint,json=data)


print(requests.get(endpoint).json())