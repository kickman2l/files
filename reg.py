import os
import requests
import json
import sys
from requests.auth import HTTPBasicAuth

zabbix_server = "192.168.33.100"
zabbix_api_admin_name = "Admin"
zabbix_api_admin_password = "zabbix"


# POST FUNCTION TO SEND REQUESTS TO API
def post(req):
    headers = {'content-type': 'application/json'}
    return requests.post(
        "http://" + zabbix_server + "/api_jsonrpc.php",
        data=json.dumps(req),
        headers=headers,
        auth=HTTPBasicAuth(zabbix_api_admin_name, zabbix_api_admin_password)
    )

# GET TOKET FOR USER
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


# CHECK IS GROUP EXISTS BY NAME
def is_groupe_exists(group_name):
    results = post({
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    group_name,
                ]
            }
        },
        "auth": auth_token,
        "id": 1
    }).json()["result"]
    return results


# CHECK IS TEMPLATE EXISTS BY NAME
def get_template_id(template_name):
    results = post({
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    template_name,
                ]
            }
        },
        "auth": auth_token,
        "id": 1
    }).json()["result"]
    return results


# CREATE CROUP WITH NAME
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


# REGISTER HOSTNAME
def register_host(hostname, ip, groupe_id, tpl_id):
    post({
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname,
            "templates": [{
                "templateid": tpl_id
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
                {"groupid": groupe_id},
            ]
        },
        "auth": auth_token,
        "id": 1
    })


def update_host(hostname, ip, groupe_id, tpl_id):
    post({
        "jsonrpc": "2.0",
        "method": "host.update",
        "params": {
            "host": hostname,
            "templates": [{
                "templateid": tpl_id
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
                {"groupid": groupe_id},
            ]
        },
        "auth": auth_token,
        "id": 1
    })

# CHECK HOSTNAME
def check_hostname(hostname):
    results = post({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    hostname,
                ]
            }
        },
        "auth": auth_token,
        "id": 1
    }).json()["result"]
    return results

# PROCESS
g_name = "CloudHostasdasdasds111222"
groupe = is_groupe_exists(g_name)
hostname = "agent.loc"
ip = "192.168.33.110"


if len(groupe) == 0:
    create_group(g_name)

groupe_id = is_groupe_exists(g_name)[0]["groupid"]

t_name = "Custom template"
template = get_template_id(t_name)

if len(template) == 0:
    tpl_id = get_template_id("Template OS Linux")[0]["templateid"]
else:
    tpl_id = template[0]["templateid"]

host = check_hostname(hostname)

if len(host) == 0:
    register_host(hostname, ip, groupe_id, tpl_id)
else:
    update_host(hostname, ip, groupe_id, tpl_id)
