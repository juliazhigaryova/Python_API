import requests
import json
import pprint

# 1 GitHub API
url = 'https://api.github.com/users/juliazhigaryova/repos'
params = {'type':'owner'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

response = requests.get(url,headers=headers,params=params)
j_data = response.json
with open('data.json', 'w') as f:
    json.dump(j_data, f)

# 2 Foursquare REST API v2
url = 'https://api.foursquare.com/v2/venues/explore'
client_id = 'LENZ3DFFAPKEYSYFKGMO23BX1CSFWYSZ4QFKRNIZIPPSF5QR'
client_secret = 'MGLKDSU2C1L5T1WTX2I31J2UYTJGGDIOKHL310Z2QNLKZFU0'
params = dict(
client_id=client_id,
client_secret=client_secret,
v='20180323',
ll='40.7243,-74.0018',
query='coffee',
limit=1
)
response = requests.get(url,headers=headers,params=params)
data = response.text
with open('text.json', 'w') as f:
    json.dump(data, f)

