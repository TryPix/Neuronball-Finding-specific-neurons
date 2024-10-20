import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import csv

def get_player_options(script):
    if not script: return

    script_content = script.string
    match = re.search(r'var\s+player_options\s*=\s*({.*?});', script_content, re.DOTALL)

    if match:
        player_options = match.group(1)  # Get the contents inside the braces

        player_options = player_options.replace("'", '"')  # Replace single quotes with double quotes
        player_options = re.sub(r'(\w+)\s*:', r'"\1":', player_options)  # Quote unquoted property names

        player_options_dict = json.loads(player_options)
    
    return player_options_dict

def get_stats(stats):
    if not stats: return

    stats_dict = {}
    for stat in stats.find_all('div'):
        stat_name = stat.contents[0].strip()
        stat_value = stat.find('span').text.strip()
        stats_dict[stat_name] = int(stat_value)

    return stats_dict

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    name_div = soup.find('div', class_= 'neuron-name')
    neuron_type_div = soup.find('div', class_ = 'neuron-type')
    stats_div = soup.find('div', class_ = 'stats')
    script_div = soup.find('div', class_ = 'content').find('script')
    level_div = soup.find('div', class_ = 'level')
    world_rank = soup.find('div', class_ = 'ranked')
    
    if world_rank: world_rank = world_rank.find('i', class_='fa fa-globe').find_parent('tr').find_all('td')[2]

    if (not name_div): return

    player_full_info = {"Name": name_div.text, "Type": neuron_type_div.text}
    player_full_info.update(get_player_options(script_div))
    player_full_info.update(get_stats(stats_div))
    player_full_info['level'] = level_div.text.replace('level ', '')

    if world_rank:
        world_rank_int = world_rank.text.replace('#', '')
        player_full_info['rank'] = world_rank_int
    else:
         player_full_info['rank'] = 0

    return player_full_info

def get_all(start_id, end_id):
     with open('neuron_database.csv', mode='a', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)
       # writer.writerow(['id', 'Name', 'Type', 'pattern', 'color1', 'color2', 'number', 'type_id', 'eyes', 'Goals', 'Passes', 'Interceptions', 'Framed Shots', 'Stopped Shots', 'level', 'rank'])


        for neuron_id in range(start_id, end_id):
            url = f'https://www.neuronball.com/en/player/{neuron_id}/'
            player_info = {"id": neuron_id}
            data = get_data(url)
            if data:
                player_info.update(data)

                writer.writerow(player_info.values())

                # To not overwhelm the server
                time.sleep(random.uniform(1, 3))


if __name__ == '__main__':
    get_all(14000, 14001)
