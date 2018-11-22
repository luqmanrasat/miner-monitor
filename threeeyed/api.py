import json
import requests

api_url_base = 'http://mine.threeeyed.info/api/'
headers = {'Content-Type': 'application/json'}

def get_worker_stats(wallet):
    api_url = '{0}worker_stats?{1}'.format(api_url_base, wallet)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
