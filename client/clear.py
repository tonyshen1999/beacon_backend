import requests
import json
endpoint = "http://127.0.0.1:8000/clear-calc/"
data ={
    "scn_id":1,
    "scn_version": 1,
    "entities": [
        {"entity_name":"Ferry Group","pd_name": "CYE2022",},
        {"entity_name":"USSH","pd_name": "CYE2022",}
        ]

}

requests.post(endpoint,json=data)