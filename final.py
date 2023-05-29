from bs4 import BeautifulSoup
import re
import os
import requests
directory = 'your_directory'
roi = 'no info on the website'
url = 'https://koober.com/en/resumes'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
sorpa = BeautifulSoup(response.content, "html.parser")
for g in sorpa.find_all(class_='bage__de__koob__V___2 margin-20'):
    link = 'https://koober.com' + g.find(class_='anchor__badge__de__koob')['href']
    title = g.find(class_='row-fluid font-size-15 title').text.strip()
    author = g.find_all(class_='row-fluid font-size-10 auteur')[0].text.replace('de ','').strip()
    if author == '':
        author = roi
    writer = g.find_all(class_='row-fluid font-size-10 auteur')[1].text.replace('par ','').strip()
    if writer == '':
        writer = roi
    time = g.find(class_='row-fluid bottom-div').text.strip()
    img = g.find('img')['src']
    bf = re.sub(r"[^\w\s]", "", title)
    file_name = os.path.join(directory, f"{bf}.txt")
    suffix = 1
    while os.path.exists(file_name):
        file_name = os.path.join(directory, f"{bf} ({suffix}).txt")
        suffix += 1
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Link: {link}\n")
        file.write(f"Title: {title}\n")
        file.write(f"Author of the book: {author}\n")
        file.write(f"Author of the summary: {writer}\n")
        file.write(f"Book cover: {img}\n")
        file.write(f"Time to read: {time}\n")
    