import requests
# from bs4 import BeautifulSoup
import json
address = input("give me your address")
parts = address.split(" ")
state = input("give me your state/city")
url1 = "https://api4.ballotpedia.org/geocode?location="+ parts[0] + "%20"+ parts[1] +"%20" + parts[2] + "%20" + state
session = requests.Session()

response = session.get(url1)
formatted_headers1 = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'access-control-request-headers' : 'content-type',
    'access-control-request-method': 'GET',
    'origin': 'https://ballotpedia.my.vote',
    'referer': 'https://ballotpedia.my.vote/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

response = session.get(url1, headers=formatted_headers1)
data = json.loads(response.text)
lat = data['data']['geometry']['location']['lat']
lng = data['data']['geometry']['location']['lng']
url2 = "https://api4.ballotpedia.org/myvote_redistricting?long=" + str(lng) + "&lat=" + str(lat) + "&include_volunteer=true"
formatted_headers2 = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://ballotpedia.my.vote',
    'referer': 'https://ballotpedia.my.vote/',
    'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


response = requests.get(url2, headers=formatted_headers2)
data = json.loads(response.text)

candidates = []
if 'elections' in data['data']:
    for election in data['data']['elections']:
        for district in election['districts']:
            if 'races' not in district:
                continue
            for race in district['races']:
                for candidate in race['candidates']:
                    print(candidate['person']['name'])
