from reprlib import recursive_repr
import json
import requests


_url = 'https://rickandmortyapi.com/api/character'

def get_info(link):
    characters=requests.get(link).json()
    return characters.get('results',[])

def _data(data):
    character = data['name']
    episode = data['episode']
    episode_names = list()

    for e in episode:
        episode_names.append(e)
    return character, episode_names

def result(link):
    final_result = dict()
    for i in get_info(link):
        _name, episode = _data(i)
        final_result[_name] = episode
    return final_result


final_result=result(_url)

with open('episode.json', 'w') as file:
    json.dump(final_result, file, indent=4)





