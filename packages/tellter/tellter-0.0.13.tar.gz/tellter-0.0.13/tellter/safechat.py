import requests

def vulgar(text):
    r = requests.get("http://dedicated.dcounter.space:3838/check/"+text)
    return int(r.json())
