#########################################################################################################
# The code can be used for patching vms with particular entity (though u can modify to patch any entity)
#########################################################################################################

import json
import requests
import urllib3
import secrets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = secrets.username
password = secrets.password

category_name = "DR"
value = "GOLD"
headers = {'content-type': 'application/json'}
PC1 = secrets.PC1
PC2 = secrets.PC2


def get_vm_config(vm_uuid):
    url = f"https://{PC1}:9440/api/nutanix/v3/vms/{vm_uuid}"
    resp = requests.get(url, verify=False, auth=(username, password), headers=headers)
    if resp.status_code != 200:
        print('VM does not exist !!!')
    else:
        json_resp = resp.json()  
        # pretty_json = json.dumps(json_resp, indent=4) 
        # print(pretty_json)      #<------------------- formatted json 
        return json_resp

def patch_vm_config(vm_uuid, payload):
    url = f"https://{PC1}:9440/api/nutanix/v3/vms/{vm_uuid}"
    # edit payload 
    del payload['status']
    payload['metadata']['categories_mapping'] = {category_name: [value]}
    payload['metadata']['categories'] = {category_name: value}

    # pretty_payload = json.dumps(payload, indent=4)
    # print(pretty_payload)      #<------------------- formatted json

    resp = requests.put(url, data= json.dumps(payload), verify=False, headers=headers, auth=(username, password))
    print('vm _pathing status : ', resp)


def get_vms_on_cluster(cluster_uuid):
    pass

def fetch_entity_with_cat(entity='vm'):
    # payload = {
    # "kind": entity,
    # "filter": "category_name==DG_test;category_value==GroupA",     # <---------- uncomment if want to apply filter
    # "length": 500
    # }
    payload = {
    "kind": entity,
    "length": 500,
    "filter": "num_threads_per_core==4"
    }
    url = f"https://{PC1}:9440/api/nutanix/v3/{entity}s/list"
    resp = requests.post(url, verify=False, auth=(username,password),headers=headers, json=payload )
    print(resp.status_code)
    json_resp = resp.json()
    pretty_json = json.dumps(json_resp, indent=4)
    print(pretty_json)
    return resp


fetch_entity_with_cat()