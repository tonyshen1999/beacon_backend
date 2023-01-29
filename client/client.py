import requests
import json
endpoint = "http://127.0.0.1:8000/calc/"
data ={
    "entity_name":"Ferry Group",
    "pd_name": "CYE2022",
    "scn_id":1,
    "scn_version": 1
}

requests.post(endpoint,json=data)



# print(requests.get(endpoint,data).json())