import requests

riot_developer_api_url = 'http://ddragon.leagueoflegends.com'
versions_route = '/api/versions.json'

version = requests.get(riot_developer_api_url + versions_route).json()[0]

champions_route = f'/cdn/{version}/data/en_US/champion.json'
champions = requests.get(riot_developer_api_url + champions_route).json()['data'].keys()

# write wordlist to file
with open('data/champions.txt', 'w') as f:
    for champion in champions:
        f.write(champion + '\n')
