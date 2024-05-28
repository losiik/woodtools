import json

import requests
import time

base_url = "https://web.archive.org/web/20221007064311/http://woodtools.nov.ru/"

base_pdf_path = 'pdfs/'
# Имя файла, из которого будет прочитан JSON
file_name = 'data.json'

links = []

# Чтение данных из JSON-файла
with open(file_name, 'r', encoding='utf-8') as json_file:
    links = json.load(json_file)

pdf_links = [link for link in links if '.pdf' in link['link']]

for i, link in enumerate(pdf_links):
    print(i)
    if i >= 111:
        response = requests.get(base_url + link['link'])
        # Проверка успешности запроса
        if response.status_code == 200:
            # Открытие файла в режиме записи байтов
            title = link['title']
            title = title.replace(" ", "_")
            title = title.replace("/", "_")
            title = title.replace("\n", "")
            title = title.replace('"', "")
            title += '.pdf'
            with open(base_pdf_path + title, 'wb') as file:
                # Запись содержимого файла в локальный файл
                file.write(response.content)
                print(title)
                time.sleep(1)
