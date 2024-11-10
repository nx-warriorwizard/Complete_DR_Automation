#####################################################################################################
# The code can be used for creating recovery plan
# fetch the az url i.e., cluster url i.e., uuid of unnmaed cluster present (idk why)
# fetch uuid of cluster pass it
# few things I'm assuming ( witness is default central )
# network is hardcode using primary ( minute change can be edited)
# category is hard coded and ( failing is on automatic basis 30 sec )
#####################################################################################################

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


def get_cluser_url(PC=PC1):
    URL= f'https://{PC}:9440/api/nutanix/v3/clusters/list'
    payload = {
        "kind": "cluster",
        "filter": "name== unnamed"
    }
    #### filter not working for cluster name
    resp= requests.post(URL, verify=False, auth=(username,password), headers=headers, json=payload)
    if resp.status_code == 200 :
        for cluster in resp.json()['entities']:
            if cluster['spec']['name'] == 'Unnamed':
                print(f"cluster url == {cluster['metadata']['uuid']}")
                return cluster['metadata']['uuid']
    else:
        print('can connect, check ')

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

def get_recovery_plan(PC=PC1):
    URL= f'https://{PC}/api/nutanix/v3/recovery_plans/list'
    payload = {
        "kind": "recovery_plan"
    }
    resp = requests.post(URL, verify=False, auth=(username,password), headers=headers, json=payload)
    if resp.status_code ==200:
        print(json.dumps(resp, indent=4))
    else:
        print("can't fetch recovery plan")


def create_recovery_plan(cluster_url,cluster_1_uuid, cluster_2_uuid,PC=PC1):
    URL=f'https://{PC}:9440/api/nutanix/v3/recovery_plans'
    payload = {
        "spec": {
            "name": "amt_recovery",
            "resources": {
                "stage_list": [
                    {
                        "delay_time_secs": 0,
                        "stage_work": {
                        "recover_entities": {
                            "entity_info_list": [
                            {
                                "categories": {
                                "DR": "SILVER"
                                }
                            }
                            ]
                        }
                        }
                    }
                ],
                "parameters": {
                            "availability_zone_list": [
                            {
                                "availability_zone_url": f"{cluster_url}",
                                "cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": f"{cluster_1_uuid}"
                                }
                                ]
                            },
                            {
                                "availability_zone_url": f"{cluster_url}",
                                "cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": f"{cluster_2_uuid}"
                                }
                                ]
                            }
                            ],
                            "data_service_ip_mapping_list": [],
                            "network_mapping_list": [
                            {
                                "availability_zone_network_mapping_list": [
                                {
                                    "availability_zone_url": f"{cluster_url}",
                                    "cluster_reference_list": [
                                    {
                                        "kind": "cluster",
                                        "uuid": f"{cluster_1_uuid}"
                                    }
                                    ],
                                    "recovery_network": {
                                    "name": "Primary"
                                    }
                                },
                                {
                                    "availability_zone_url": f"{cluster_url}",
                                    "cluster_reference_list": [
                                    {
                                        "kind": "cluster",
                                        "uuid": f"{cluster_2_uuid}"
                                    }
                                    ],
                                    "recovery_network": {
                                    "name": "Primary"
                                    }
                                }
                                ]
                            }
                            ],
                            "primary_location_index": 0,
                            "witness_configuration_list": [
                            {
                                "witness_address": f"{cluster_url}",
                                "witness_failover_timeout_secs": 30
                            }
                            ]
                        }
                }
        },
        "metadata": {
            "kind": "recovery_plan",
            "spec_version": 0
        }
    }
    resp= requests.post(URL, verify=False, auth=(username, password), headers=headers, json=payload)
    if resp.status_code== 202:
        print('recovery plan creation in process')
    else:
        print("can't create please check")

# get_recovery_plan()
cluster_url = get_cluser_url()
print(fetch_cluster_uuid())
create_recovery_plan(cluster_url ,cluster_1_uuid="00062487-d917-b3d3-776a-7cc25530ea93",cluster_2_uuid="0006264e-0fc6-1949-0000-000000011597", PC=PC1)

