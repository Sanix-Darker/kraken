import requests
import argparse
import json

# Initialize the arguments
# Example command python req.py -u https://google.com?q=test
prs = argparse.ArgumentParser()
prs.add_argument('-u', '--url', help='THe link of the requests you want to perform', type=str, required=True)
prs.add_argument('-m', '--method', help='The method (GET, POST, etc...) ', type=str, default="GET")
prs.add_argument('-d', '--data', help='The data you want to post (A JSON STRING)', type=int, default="{}")
prs = prs.parse_args()

print("[+] Sending a requests...")
result = ""
if prs.method.upper() == "GET":
    result = requests.get(prs.url).content.decode("utf-8")
elif prs.method.upper() == "POST":
    result = requests.post(prs.url, json=json.loads(prs.data)).content.decode("utf-8")

print(result)
