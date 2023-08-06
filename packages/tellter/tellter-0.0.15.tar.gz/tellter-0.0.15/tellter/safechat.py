import requests

def vulgar(text):
    query = text.replace("?", "-")
    r = requests.get("http://dedicated.dcounter.space:3838/check/"+query)
    return int(r.json())
