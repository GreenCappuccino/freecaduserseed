import requests
import csv

url = "https://wiki.freecad.org/api.php?action=query&format=json&list=allusers"
headers = {
    "User-Agent": "get_wiki_users.py"}

# Make initial request
response = requests.get(url, headers=headers).json()
users = response["query"]["allusers"]

# Keep making requests until all users have been retrieved
while "continue" in response:
    continue_params = response["continue"]
    continue_url = url + "&aufrom=" + continue_params["aufrom"] + "&continue=" + continue_params["continue"]
    response = requests.get(continue_url, headers=headers).json()
    users += response["query"]["allusers"]

# Export users as TSV
with open("wiki_users.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["userid", "name"])
    for user in users:
        writer.writerow([user["userid"], user["name"]])
