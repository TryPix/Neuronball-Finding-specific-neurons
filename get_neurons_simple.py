import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import csv
import os

def get_neuron_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    neurons_div = soup.find('div', class_ = 'detailed-team-players clearfix')

    if (not neurons_div): return

    names_div = neurons_div.find_all('div', class_ = 'neuron-name')
    levels_div = neurons_div.find_all('div', class_ = 'neuron-lv')
    scripts_div = neurons_div.find_all('script')

    data = []

    for i in range(0, len(names_div)):
        name = names_div[i].text
        level = levels_div[i].text.replace('Level: ', '')

        player_id_match = re.search(r'var player(\d+)', scripts_div[i].string)
        player_id = player_id_match.group(1)

        params_pattern = re.compile(r'pattern:\s*(\d+),\s*color1:\s*"(#\w+)",\s*color2:\s*"(#\w+)",\s*number:\s*(\d+),\s*eyes:\s*(\d+),\s*type_id:\s*(\d+)')
        params_match = params_pattern.search(scripts_div[i].string)

        neuron_info = {
            "player_id": player_id,
            "pattern": int(params_match.group(1)),
            "color1": params_match.group(2),
            "color2": params_match.group(3),
            "number": int(params_match.group(4)),
            "eyes": int(params_match.group(5)),
            "type_id": int(params_match.group(6)),
        }

        neuron_info.update({'name':name, 'level':level})
        data.append(neuron_info)

    return data

def to_csv(data, output_file = 'neuron_database_simple.csv'):

    file_exists = os.path.exists(output_file)

    with open(output_file, 'a', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if not file_exists: dict_writer.writeheader()
        dict_writer.writerows(data)

def get_all(start, end):
    for i in range(start, end):
        url = f'https://www.neuronball.com/en/team/{i}/'
        data = get_neuron_data(url)
        if data: to_csv(data)
        time.sleep(random.uniform(3, 5))

if __name__ == '__main__':
    get_all(10, 11)
