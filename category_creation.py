#########################################################################################################
# The code can be used for creating category creation 
# for creating category first create category key and then create category value
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


def get_cat_key(category_name):
    url = f'https://{PC1}:9440/api/nutanix/v3/categories/{category_name}'
    resp = requests.get(url,headers=headers, auth=(username,password), verify=False)
    if resp.status_code != 200:
        print('This key does not exist ')
    return resp

def get_cat_val(category_name, value):
    url = f'https://{PC1}:9440/api/nutanix/v3/categories/{category_name}/{value}'
    resp = requests.get(url,headers=headers, auth=(username,password), verify=False)
    if resp.status_code != 200:
        print('This val does not exist ')
    return resp

def create_cat_key(category_name):
    payload = {
        "description": "string",
        "capabilities": {
            "cardinality": 1
        },
        "name": f'{category_name}'
        }
    url = f'https://{PC1}:9440/api/nutanix/v3/categories/{category_name}'
    resp = requests.put(url, verify=False, headers=headers, auth=(username,password),json= payload)
    if get_cat_key(category_name).status_code ==200:
        print('category key created succesfully !!!')
    return resp

def create_cat_val(category_name, value):
    payload = {
        "value": f'{value}'
    }
    url = f'https://{PC1}:9440/api/nutanix/v3/categories/{category_name}/{value}'
    resp = requests.put(url, verify=False, headers=headers, auth = (username,password), json = payload)
    if get_cat_val(category_name,value).status_code ==200:
        print('category value created succesfully !!!')
    return resp



create_cat_key('DR')
create_cat_val('DR','GOLD')
create_cat_val('DR','SILVER')