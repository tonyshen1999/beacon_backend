import requests

endpoint = "http://127.0.0.1:8000/entity/"
pd_data = {
    'period': 'CYE2017', 
    'begin_date': '2017-01-01', 
    'end_date': '2017-12-31'
}
response = requests.get(endpoint)

print(response.json())