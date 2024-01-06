import re
import json
import requests
from bs4 import BeautifulSoup

from datetime import date

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask


env_path = Path('.') / '.env'
load_dotenv()

app = Flask(__name__)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

message = [ 'array hooray' ]

# URL to scrape
url = 'https://www.airnewzealandnewsroom.com/'

# Send a GET request to the URL
response = requests.get(url)


message = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div items and print their content
    div_items = soup.find_all("script")

    # Define a regular expression pattern to match everything after 'blocklistitems'
    
    strung = str(div_items)

    sub1 = "var blocklistitems ="
    sub2 = ";blocklistitems.id"   

    s=str(re.escape(sub1))
 
    e=str(re.escape(sub2))

    res=re.findall(s+"(.*)"+e,strung)[0]

    mobject = json.loads(res)

    message.append(mobject)

    json_formatted_str = json.dumps(message, indent=2)

#    print(json_formatted_str)

else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")



today = date.today()

print (today)

heute = str(today)

Json_filter = []
#for i in json_formatted_str:
#    for items
#    Json_filter.append(app_data)

for i in mobject["items"]:
    if i["FilterDate"] == "2023-11-30":   
        Json_filter.append(i)

print(Json_filter)

for item in Json_filter:
    title = item.get("Title", "")
    url = item.get("URL", "")
    abstract = item.get("Abstract", "")
    filter_date = item.get("FilterDate", "")
    sort = item.get("Sort", "")

# Now you can use the variables as needed
print(f"Title: {title}")
print(f"URL: {url}")
print(f"Abstract: {abstract}")
print(f"FilterDate: {filter_date}")
print(f"Sort: {sort}")


#    for key, value in item.items():
#        print(f"{key}: {value}")

SLK = f"hello here's your news:", title


#print(mobject["items"])



client.chat_postMessage(channel='#bot', text=heute)

client.chat_postMessage(channel='#bot', blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": title}}])

#if __name__ == "__main__":
#    app.run(debug=True)