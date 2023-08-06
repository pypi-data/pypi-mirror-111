import requests

def vulgar(text, sensitivity):
    query = text.replace("?", "-")
    r = requests.get("http://dedicated.dcounter.space:3838/check/"+str(sensitivity)+"/"+query)
    return int(r.json())
