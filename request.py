import requests


BASE_URL = 'https://practice.geeksforgeeks.org'
API_URL = 'https://practiceapi.geeksforgeeks.org/api/v1'

def get(url,**kwargs):
    return requests.get(BASE_URL + url,**kwargs)

def post(url,**kwargs):
    return requests.post(API_URL + url,**kwargs)
