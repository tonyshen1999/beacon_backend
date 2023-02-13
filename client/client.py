import requests
import json
# endpoint = "http://127.0.0.1:8000/calc/"
# data ={
#     "scn_id":1,
#     "scn_version": 1,
#     "entities": [
#         {"entity_name":"Ferry Group","pd_name": "CYE2022",},
#         {"entity_name":"USSH","pd_name": "CYE2022",}
#         ]

# }

# requests.post(endpoint,json=data)


# endpoint = "http://127.0.0.1:8000/log/"
# data = {
#     'period': 'CYE2022', 
#     'entity': 'USSH', 
#     'scn_id': '1', 
#     'scn_version': '1'}

# print(requests.get(endpoint,params=data).json())

# endpoint = "http://127.0.0.1:8000/import-log/"
# print(requests.get(endpoint).json())

# endpoint = "http://127.0.0.1:8000/scn-list/"

# print(requests.get(url=endpoint).json())

# print(requests.get(endpoint,data).json())

# endpoint = "http://127.0.0.1:8000/calc-log-list/"
# data ={
#     "scn_id":90,
#     "scn_version": 1,

# }

# print(requests.get(endpoint,params=data).json())

# endpoint = "http://127.0.0.1:8000/acc/"
# data ={
#     "scn_id":90,
#     "version": 1,

# }

# print(requests.get(endpoint,params=data).json())

# endpoint = "http://127.0.0.1:8000/scn-notes/"
# data ={
#     "scn_id":90,
#     "version": 4,
#     "description": "test if this shit updated"

# }

# print(requests.put(endpoint,params=data).json())

# get_data ={
#     "scn_id":90,
#     "version": 4,
#     "description": "test if this shit updated"

# }

# print(requests.get(endpoint,params=get_data).json())

endpoint = "http://127.0.0.1:8000/clone-scn/"
data ={
    "scn_id":5,
    "new_id":60,
    "new_name":"wut"

}

requests.post(endpoint,json=data)