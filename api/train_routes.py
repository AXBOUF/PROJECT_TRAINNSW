'''
https://opendata.transport.nsw.gov.au/data/dataset/3e349c1c-9ac0-4f70-8a3f-b1d3e4cb1042/resource/1c2b217e-d0c1-4626-962e-55b73cbbe732/download/sydneytrains.json

'''

import requests
import load_dotenv as dotenv
import os
import json

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

# we are going to use link above to download the json file 
url = "https://opendata.transport.nsw.gov.au/data/dataset/3e349c1c-9ac0-4f70-8a3f-b1d3e4cb1042/resource/1c2b217e-d0c1-4626-962e-55b73cbbe732/download/sydneytrains.json"
headers = {
    "Authorization": f"apikey {API_KEY}"
}
response = requests.get(url, headers=headers)

# lets check the response status code
# just test the call to the api 
# test 200 or not thats it
# lets download the json file success 200
# cant we just download the json file and save it to disk instead of making an api call every time we want to read the data
if response.status_code == 200:
    data = response.json()
    with open("sydneytrains.json", "w") as f:
        json.dump(data, f)
    print("Data downloaded and saved to sydneytrains.json")
else:
    print("API request failed with status code:", response.status_code)