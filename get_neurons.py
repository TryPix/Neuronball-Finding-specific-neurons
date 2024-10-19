import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import csv

url = 'https://www.neuronball.com/en/player/1391757/'

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

    if (not name_div): return

    player_full_info = {"Name": name_div.text, "Type": neuron_type_div.text}

    player_full_info.update(get_player_options(script_div))
    player_full_info.update(get_stats(stats_div))

    return player_full_info

def get_all(start_id, end_id):
     with open('neuron_database.csv', mode='a', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)
       # writer.writerow(['id', 'Name', 'Type', 'pattern', 'color1', 'color2', 'number', 'type_id', 'eyes', 'Goals', 'Passes', 'Interceptions', 'Framed Shots', 'Stopped Shots'])


        for neuron_id in range(start_id, end_id):
            url = f'https://www.neuronball.com/en/player/{neuron_id}/'
            player_info = {"id": neuron_id}
            data = get_data(url)
            if data:
                player_info.update(get_data(url))

                writer.writerow(player_info.values())

                # To not overwhelm the server
                time.sleep(random.uniform(0.75, 1))


if __name__ == '__main__':
    get_all(14000, 14010)
