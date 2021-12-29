"""
Integration between Brewfather and Minibrew.
Allows keg temperatures to be read into Brewfather.

TotalSmart 2021
"""
import requests
import json
import time

MINIBREW_USERNAME = ""
MINIBREW_PASSWORD = ""

# login to pro portal and can be located with chrome developer tools.
MINIBREW_TOKEN = ""

# Can be found after "id=' in custom endpoint configuration.
BREWFATHER_ENDPOINT_ID = ""


def send_to_brewfather(keg_name, target_temp, current_temp):
    url = "http://log.brewfather.net/stream?id=" + BREWFATHER_ENDPOINT_ID

    payload = json.dumps({
        "name": keg_name,
        "temp": current_temp,
        "aux_temp": target_temp,
        "temp_unit": "C",
        "beer": "Test Beer"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def minibrew_login():
    headers = {
        'Authorization': 'TOKEN '+ MINIBREW_TOKEN,
        'Content-Type': 'application/json'
    }
    params = {}

    data = json.dumps({
        "email": MINIBREW_USERNAME,
        "password": MINIBREW_PASSWORD
    })

    url = "https://api.minibrew.io/v2/token/"
    response = requests.request("POST", url, data=data, headers=headers)
    response_dict = response.json()
    token_api = response_dict['token']

    return token_api


def minibrew_info(api):
    url = "https://api.minibrew.io/v1/breweryoverview/"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + api,
        'client': 'Breweryportal',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)
    resp_dict = response.json()
    return resp_dict
    #send_to_brewfather(resp_dict['fermenting'][0]['target_temp'], resp_dict['fermenting'][0]['current_temp'])


def get_keg_info(minibrew_info):
    keg_states = []
    for keg in minibrew_info['fermenting']:
        keg_states.append({
            'name': keg['title'],
            'current_temp': keg['current_temp'],
            'target_temp': keg['target_temp']
        })
    return keg_states

while True:
    token = minibrew_login()
    print("Getting info")
    info = minibrew_info(token)
    kegs = get_keg_info(info)
    if kegs:
        for keg in kegs:
            print(f"Updating {keg['name']} on Brewfather")
            send_to_brewfather(keg['name'], keg['target_temp'], keg['current_temp'])
    print("Sleeping...")
    time.sleep(900)






