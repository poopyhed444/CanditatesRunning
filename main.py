import requests
import json
import asyncio
import random
from GetOutput import test


async def process_candidates(candidates):
    tasks = []
    for candidate_name in candidates:
        wait_time = random.uniform(1, 5)
        await asyncio.sleep(wait_time)
        task = asyncio.create_task(test(candidate_name))
        tasks.append(task)
    await asyncio.gather(*tasks)

def get_candidates(address, state):
    parts = address.split(" ")
    url1 = "https://api4.ballotpedia.org/geocode?location=" + parts[0] + "%20" + parts[1] + "%20" + parts[2] + "%20" + state

    session = requests.Session()
    formatted_headers1 = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'access-control-request-headers': 'content-type',
        'access-control-request-method': 'GET',
        'origin': 'https://ballotpedia.my.vote',
        'referer': 'https://ballotpedia.my.vote/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    try:
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
                for district in election.get('districts', []):
                    if district['races'] is None:
                        continue
                    for race in district['races']:
                        for candidate in race['candidates']:
                            candidates.append(candidate['person']['name'])

        return candidates

    except Exception as e:
        print("Sorry, Ballotpedia is not currently covering any upcoming elections in your area or perhaps you have entered the wrong address.")
        return []


if __name__ == "__main__":
    address = input("Give me your address: ")
    state = input("Give me your state/city: ")

    candidates = get_candidates(address, state)
    if candidates:
        print("Here are your candidates for your area (This may take a while due to rate limitations): " )
        asyncio.run(process_candidates(candidates))
