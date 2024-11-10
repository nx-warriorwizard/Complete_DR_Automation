#########################################################################################################
# The code can be used for creating subnets on various clusters
# this is very minimal implementation srry :) 

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


def fetch_cluster_uuid(PC=PC1):
    payload = {"kind": "cluster"}
    URL = f"https://{PC}:9440/api/nutanix/v3/clusters/list"
    resp = requests.post(URL, json=payload, headers=headers, verify=False, auth=(username,password))
    # print(resp.json())
    clusters= {}
    if resp.status_code == 200:
        for entity in resp.json()['entities']:
            clusters[entity['spec']['name']]= entity['metadata']['uuid']
    return clusters.items()

def create_subnet(cluster_uuid,PC=PC1, subnet_name='test1-amt'):
    payload = {
        "spec": {
            "name": subnet_name,
            "resources": {
            "subnet_type": "VLAN"
            },
            "cluster_reference": {
            "uuid": cluster_uuid,
            "kind": "cluster"
            }
        },
        "metadata": {
            "kind": "subnet"
        }
    }
    URL= f'https://{PC}:9440/api/nutanix/v3/subnets'
    resp=requests.post(URL, auth=(username,password), verify=False, json=payload, headers=headers)
    print('status code : ', resp.status_code)
    if resp.status_code == 202:
        print('subnet creation in process')
    else:
        print('some issue')



print(fetch_cluster_uuid(PC1))
# create_subnet('00062487-d917-b3d3-776a-7cc25530ea93',PC1, 'test1-amt')
# create_subnet('00062656-6854-07c6-3c0e-0cc47ac327e9',PC2, 'test1-amt')
create_subnet('0006264e-0fc6-1949-0000-000000011597', PC1, 'test1-amt')
