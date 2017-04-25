import os, requests, json, sys
from requests.auth import HTTPBasicAuth

zabbix_server = "192.168.33.100"
zabbix_api_admin_name = "Admin"
zabbix_api_admin_password = "zabbix"

def post(request):
    headers = {'content-type': 'application/json'}
    return requests.post(
        "http://" + zabbix_server + "/api_jsonrpc.php",
        data=json.dumps(request),
        headers=headers,
        auth=HTTPBasicAuth(zabbix_api_admin_name, zabbix_api_admin_password)
    )

auth_token = post({
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": zabbix_api_admin_name,
        "password": zabbix_api_admin_password
    },
    "auth": None,
    "id": 0}
).json()["result"]

print auth_token
