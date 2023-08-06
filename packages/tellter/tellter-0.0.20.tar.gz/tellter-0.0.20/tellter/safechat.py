import requests

class Safechat:
    def __init__(self, key):
        self.api_key = key # Defines the API key

    def vulgar(self, text, sensitivity):
        query = text.replace("?", "-")
        r = requests.get("http://dedicated.dcounter.space:3838/check/"+self.api_key+"/"+str(sensitivity)+"/"+query)
        response = r.content.decode()
        if response == "WRONG_API_KEY":
            raise APIKeyError("API Key is invalid.")
        else:
            return int(response)
