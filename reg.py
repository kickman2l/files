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

def is_groupe_exists():
    post({
    "jsonrpc": "2.0",
    "method": "hostgroup.exists",
    "params": {
        "name": ["SUPERSTAR YEAH!"]
    },
    "auth": auth_token,
    "id": 1
})

def create_group(groupe_name):
    post({
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": {
            "name": groupe_name
        },
        "auth": auth_token,
        "id": 1
    })

def register_host(hostname, ip):
    post({
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname,
            "templates": [{
                "templateid": "10001"
            }],
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }],
            "groups": [
                {"groupid": "1"},
                {"groupid": "2"}
            ]
        },
        "auth": auth_token,
        "id": 1
    })

data = is_groupe_exists()
#create_group("SUPERSTAR YEAH!")
print data
# register_host('agent.loc','192.168.33.110')
