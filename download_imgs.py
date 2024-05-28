import json
import time

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile


base_url = "http://woodtools.nov.ru/"

base_pdf_path = 'imgs/'
# Имя файла, из которого будет прочитан JSON
file_name = 'data.json'

links = []

# Чтение данных из JSON-файла
with open(file_name, 'r', encoding='utf-8') as json_file:
    links = json.load(json_file)

htm_links = [link for link in links if '.htm' in link['link']]

for i, link in enumerate(htm_links):
    if i > 450:
        response = requests.get(base_url + link['link'])
        soup = BeautifulSoup(response.content, "html.parser")
        a_tags = soup.find_all('a')
        links = [a.get('href') for a in a_tags if a.get('href')]
        img_links = [l for l in links if "http" not in l and "htm" in l]
        print(img_links)
        add_link = link['link'].split("/")
        add_link.pop()
        add_link = "/".join(add_link)

        src_values = []
        for img_link in img_links:
            r = requests.get(base_url + add_link + "/" + img_link)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')

                # Извлечение значений src из тегов <img>
                for img_tag in soup.find_all('img'):
                    src = img_tag.get('src')
                    if src:
                        src_values.append(src)

        images = []
        for src in src_values:
            response_img = requests.get(base_url + add_link + "/" + src)
            if response_img.status_code == 200:
                try:
                    image = Image.open(BytesIO(response_img.content))
                    images.append(image)
                except:
                    pass

        if images != []:
            title = link['title']
            title = title.replace(" ", "_")
            title = title.replace("/", "_")
            title = title.replace("\n", "")
            title = title.replace('"', "")
            title += '.pdf'

            pdf_filename = base_pdf_path + title
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter

            for img in images:
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height
                if img_width > width or img_height > height:
                    if img_width > img_height:
                        img_width = width
                        img_height = width / aspect_ratio
                    else:
                        img_height = height
                        img_width = height * aspect_ratio

                img = img.resize((int(img_width), int(img_height)))

                # Сохранение изображения во временный файл
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
                    img.save(tmpfile, format='JPEG')
                    tmpfile_path = tmpfile.name

                c.drawImage(tmpfile_path, 0, height - img_height, width=img_width, height=img_height)
                c.showPage()

            c.save()
            print(title)

