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


endpoint = "http://127.0.0.1:8000/log/"
data = {
    'period': 'CYE2022', 
    'entity': 'USSH', 
    'scn_id': '1', 
    'scn_version': '1'}

print(requests.get(endpoint,params=data).json())



# endpoint = "http://127.0.0.1:8000/scn-list/"

# print(requests.get(url=endpoint).json())

# print(requests.get(endpoint,data).json())