import csv

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

# Replace these with your login credentials
username = "MemberlistParsingBot"
password = "<REDACTED>"

# The URL of the login form
login_url = "https://forum.freecad.org/ucp.php?mode=login"

# Create a session object
session = requests.Session()

print("Created a browsing session.")

# Retrieve sid, form_token, creation_time
response = session.get(login_url)
soup = BeautifulSoup(response.content, "html.parser")
sid = soup.find("input", {"name": "sid"})["value"]
form_token = soup.find("input", {"name": "form_token"})["value"]
creation_time = soup.find("input", {"name": "creation_time"})["value"]

print(f"Retrieved from login form\n"
      f"sid: {sid}\n"
      f"form_token: {form_token}\n"
      f"creation_time: {creation_time}")

# The data to send in the POST request
login_data = {
    "login": "Login",
    "username": username,
    "password": password,
    "sid": sid,
    "form_token": form_token,
    "creation_time": creation_time,
    "redirect": "test",
}

# Send the login POST request using the session
response = session.post(login_url, data=login_data)

print(f"Sent login form, redirected to: {response.url}")

if "sid" not in parse_qs(urlparse(response.url).query):
    soup = BeautifulSoup(response.content, "html.parser")
    print(f"Login failed: {soup.find('div', class_='error').get_text(strip=True)}")
    exit(1)

# Attempt to retrieve sid from redirect
new_sid = parse_qs(urlparse(response.url).query)["sid"][0]
print(f"Login succeeded: new sid: {new_sid}")

# Check if the login was successful
if parse_qs(urlparse(response.url).query)["sid"]:
    print("Login successful")
else:
    print("Login failed")
    exit(1)

# Load memberlist
memberlist_url = "https://forum.freecad.org/memberlist.php"
response = session.get(memberlist_url)
soup = BeautifulSoup(response.content, "html.parser")

pagination = soup.find("div", class_="pagination")
total_users = int(pagination.get_text(strip=True).split()[0])

# Calculate number of pages
members_per_page = 25
num_pages = total_users // members_per_page + (1 if total_users % members_per_page != 0 else 0)
print(f"Total users: {total_users}")
print(f"Number of pages: {num_pages}")

rows = [["username", "rank", "posts", "website", "joined"]]

# Begin retrieving memberlist information
for page_i in range(num_pages):
    url_paginated = urlunparse(urlparse(memberlist_url)._replace(
        query=urlencode(dict(parse_qs(urlparse(memberlist_url).query), start=[f"{page_i * members_per_page}"]),
                        doseq=True)))
    print(f"Fetching: {url_paginated}")
    response = session.get(url_paginated)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "memberlist"})
    tbody = table.find("tbody")
    for row in tbody.find_all("tr"):
        columns = row.find_all("td")
        rows.append([column.get_text(strip=True) for column in columns])
    print(f"Total Rows: {len(rows)}")

# Write rows to TSV
print("Writing data to TSV")
with open("phpbb_users.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    for row in rows:
        writer.writerow(row)
