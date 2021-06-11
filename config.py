import json
import configparser
import os
from rich import print as rprint

try:
    dirname = os.path.dirname(__file__) 
    config  = configparser.ConfigParser()
    path = os.path.join(dirname,'config.ini')
    config.read(path)
    config_json = config['DEFAULT']['config_path']
    with open(config_json,'r') as fr:
        global configuration
        configuration = json.load(fr)
except (KeyError,FileNotFoundError):
   configuration = None


def get_cookies():
    try:
        return {
                'authtoken':configuration['authtoken'],
                'gfguserName':configuration['gfguserName']
        }
    except KeyError:
        rprint('[bold red]Please add authtoken and gfguserName field in config.json')
        exit(1)
    except TypeError:
        rprint('[bold red]config.json not set/found. Set it using gfg config [path]')
        exit(1)
