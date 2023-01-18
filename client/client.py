import requests
import json
endpoint = "http://127.0.0.1:8000/rel/"
data ={
    "parent":230,
    "child": 240,
    "ownership_percentage":12.00,
    "scenario": 1
}

requests.post(endpoint,json=data)



print(requests.get(endpoint,data).json())