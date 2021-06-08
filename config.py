import json

with open('config.json','r') as fr:
    global config
    config = json.load(fr)


def get_cookies():
    return {
            'authtoken':config['authtoken'],
            'gfguserName':config['gfguserName']
    }
