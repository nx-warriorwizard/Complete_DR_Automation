#####################################################################################################
# author : Amit Yadav
# The code contains both sync and asyn replication policy creation 
# fetch the az url i.e., cluster url i.e., uuid of unnmaed cluster present (idk why)
# fetch uuid of cluster pass it
# it auto adds vm with particular category 
# change rpo time as required 
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

def get_protection_policy(PC=PC1):
    URL= f'https://{PC}:9440/api/nutanix/v3/protection_rules/list'
    payload = {"kind": "protection_rule"}
    resp= requests.post(URL, verify=False, auth=(username,password), headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.json()
    
def create_protecion_policy_sync(cluster_url,cluster_1_uuid, cluster_2_uuid, PC=PC1):
    '''
    cluster url is availability_zone_url
    '''
    URL=f'https://{PC}:9440/api/nutanix/v3/protection_rules'

    payload_sync = {
        "spec": {
            "name": "amt-test1",
            "resources": {
                "ordered_availability_zone_list": [
                {
                    "availability_zone_url": f"{cluster_url}",
                    "cluster_uuid": f"{cluster_1_uuid}"
                },
                {
                    f"availability_zone_url": f"{cluster_url}",
                    "cluster_uuid": f"{cluster_2_uuid}"
                }
                ],
                "availability_zone_connectivity_list": [
                    {
                    "source_availability_zone_index": 0,
                    "destination_availability_zone_index": 1,
                    "snapshot_schedule_list": [
                        {
                        "recovery_point_objective_secs": 0,
                        "auto_suspend_timeout_secs": 30,
                        "snapshot_type": "CRASH_CONSISTENT"
                        }
                    ]
                    },
                    {
                    "source_availability_zone_index": 1,
                    "destination_availability_zone_index": 0,
                    "snapshot_schedule_list": [
                        {
                        "recovery_point_objective_secs": 0,
                        "auto_suspend_timeout_secs": 30,
                        "snapshot_type": "CRASH_CONSISTENT"
                        }
                    ]
                    }
                ]
            }
            },
        "metadata": {
            "spec_version": 0,
            "kind": "protection_rule"
        }
    }

    resp=requests.post(URL, verify=False, auth=(username,password), headers=headers,json=payload_sync)
    if resp.status_code == 202:
        print('creating protection policy ')
    else:
        print("couldn't create protection policy please check")

def create_protection_policy_async(cluster_url, cluster_1_uuid, cluster_2_uuid, PC=PC1):
    '''
    writing code for linear snapshots ( if needed rolling see api )
    '''
    URL=f'https://{PC}:9440/api/nutanix/v3/protection_rules'
    payload_async= {
        "spec": {
            "name": "amt-test2",
            "resources": {
                "category_filter": {
                    "type": "CATEGORIES_MATCH_ANY",
                    "params": {
                    "DR": [
                        "SILVER"
                    ]
                    }
                },
                "ordered_availability_zone_list": [
                {
                    "availability_zone_url": f"{cluster_url}",
                    "cluster_uuid": f"{cluster_1_uuid}"
                },
                {
                    "availability_zone_url": f"{cluster_url}",
                    "cluster_uuid": f"{cluster_2_uuid}"
                }
                ],
                "availability_zone_connectivity_list": [
                    {
                    "source_availability_zone_index": 0,
                    "destination_availability_zone_index": 1,
                    "snapshot_schedule_list": [
                        {
                        "recovery_point_objective_secs": 3600,
                        "auto_suspend_timeout_secs": 30,
                        "snapshot_type": "CRASH_CONSISTENT",
                        "local_snapshot_retention_policy": {
                            "num_snapshots": 1
                        },
                        "remote_snapshot_retention_policy": {
                            "num_snapshots": 1
                        }
                        }
                    ]
                    },
                    {
                    "source_availability_zone_index": 1,
                    "destination_availability_zone_index": 0,
                    "snapshot_schedule_list": [
                        {
                        "recovery_point_objective_secs": 3600,
                        "auto_suspend_timeout_secs": 30,
                        "snapshot_type": "CRASH_CONSISTENT",
                        "local_snapshot_retention_policy": {
                            "num_snapshots": 1
                        },
                        "remote_snapshot_retention_policy": {
                            "num_snapshots": 1
                        }
                        }
                    ]
                    }
                ]
            }
            },
        "metadata": {
            "spec_version": 0,
            "kind": "protection_rule"
        }
    }
    
    resp=requests.post(URL, verify=False, auth=(username,password), headers=headers,json=payload_async)
    if resp.status_code == 202:
        print('creating protection policy ')
    else:
        print("couldn't create protection policy please check")


cluster_url = get_cluser_url() #  <---- use this to get cluster url 
print(fetch_cluster_uuid())

# print(json.dumps(get_protection_policy(),indent=4))
# create_protecion_policy_sync(cluster_url,cluster_1_uuid="00062487-d917-b3d3-776a-7cc25530ea93",cluster_2_uuid="0006264e-0fc6-1949-0000-000000011597",PC=PC1 )
create_protection_policy_async(cluster_url,cluster_1_uuid="00062487-d917-b3d3-776a-7cc25530ea93",cluster_2_uuid="0006264e-0fc6-1949-0000-000000011597",PC=PC1 )