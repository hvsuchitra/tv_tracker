import requests
import requests_cache

# path when running from gui
requests_cache.install_cache(cache_name='../common/cache/api', backend='sqlite', expire_after=86400)

# requests_cache.install_cache(cache_name='../../common/cache/api', backend='sqlite', expire_after=86400)


resource_base_url = 'https://thetvdb.com'
api_base_url = 'https://api.thetvdb.com'
resource_base_url_per_ep = 'https://thetvdb.com/banners/'
headers = {}


def get_jwt():
    data = {'apikey': 'api_key', 'username': 'username',
            'userkey': 'user_key'}
    with requests_cache.disabled():
        response = requests.post(f'{api_base_url}/login', json=data)
        if response.status_code == 200:
            global headers
            jwt = response.json()['token']
            headers['Authorization'] = f'Bearer {jwt}'
            return jwt


def search_show(show_name):
    shows = requests.get(f'{api_base_url}/search/series', params={'name': show_name}, headers=headers).json()
    cols_needed = ('id', 'seriesName', 'status', 'image', 'overview', 'network', 'firstAired')
    if shows.get('Error'): return None
    yield from (
        dict(zip(cols_needed, (show.get(col) if show.get(col) is not None else 'Not Available' for col in cols_needed)))
        for
        show in shows['data'])


def get_image(url):
    return requests.get(resource_base_url + url, headers=headers).content


def get_episode_count(show_id):
    url = f'{api_base_url}/series/{show_id}/episodes/summary'
    response_json = requests.get(url, headers=headers).json()
    season_list, episode_count, *_ = response_json['data'].values()
    return season_list, int(episode_count)


def get_image_per_ep(url):
    return requests.get(resource_base_url_per_ep + url, headers=headers).content


get_jwt()
