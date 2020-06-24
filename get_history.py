import requests
import json
import datetime

history_file_path = '/home/pi/pocket-cats-hist/history'
token = "INSERT_YOUR_TOKEN_HERE"

url = "https://api.pocketcasts.com/user/history"
auth = "Bearer "+token
origin = "https://play.pocketcasts.com"

headers = {"Origin":origin,"authorization": auth, "count":"200"}

r = requests.post(url, headers=headers)

if r.status_code == 200:
    print("found ", len(r.json()['episodes']), "episodes")
    now_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%m")
    export_file_path = history_file_path+now_stamp+'.json'
    with open(export_file_path, 'w') as outfile:
        json.dump(r.json(),outfile)
        
elif r.status_code == 401:
    print("The Pocket Casts History archiver isn't working. Your token has expired.")

else:
    print("The Pocket Casts History archiver might not be working. Unexpected status code:",str(r.status_code))
