import requests
import json

## this results in a 500 Internal Server Error and I don't know why.

username = "YOUR EMAIL HERE"
pwd = "YOUR PASSWORD HERE"

url = "https://api.pocketcasts.com/user/login"

origin = "https://play.pocketcasts.com"
payload = {"email": username, "password": pwd, "scope": "webplayer"}
headers = {"Origin": origin}

r = requests.post(url, headers=headers, params = payload)

print(r.status_code)
