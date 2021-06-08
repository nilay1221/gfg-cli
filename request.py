import requests


BASE_URL = 'https://practice.geeksforgeeks.org'


def get(url,**kwargs):
    return requests.get(BASE_URL + url,**kwargs)
