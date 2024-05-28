import json

import requests
from bs4 import BeautifulSoup

#windows-1251
r = requests.get('https://web.archive.org/web/20230524204836/http://woodtools.nov.ru/index.htm')


soup = BeautifulSoup(r.content, "html.parser")

all_titles = soup.findAll('h2')
a_tags = soup.find_all('a')
links = [{"link": a.get('href'), "title": a.text, "status": "not downloaded"} for a in a_tags if a.get('href')]

file_name = 'data.json'

with open(file_name, 'w', encoding='utf-8') as json_file:
    json.dump(links, json_file, ensure_ascii=False, indent=4)
