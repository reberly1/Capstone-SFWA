import requests
from bs4 import BeautifulSoup

def scrape():
    page = requests.get('https://umbc.academicworks.com/')
    soup = BeautifulSoup(page.text, 'html.parser')
   
    #Extracts the table where all scholarship data is located
    table = soup.find(class_='full striped-table')
    
    titles = []
    name_href = table.find_all('a')
    for href in name_href:
        titles.append(href.get_text(strip=True))

    descs = []
    desc_row = table.find_all('a')
    for desc in desc_row:
        href = desc.get('href')
        descs.append("https://umbc.academicworks.com" + href)

    awards = []
    award_row = table.find_all(class_='strong h4 table__column--max-width-250')
    for row in award_row:
        awards.append(row.get_text(strip=True))

    deadlines = []
    deadline_row = table.find_all(class_='mq-no-bp-only clr block')
    for row in deadline_row:
        deadlines.append(row.get_text(strip=True))

    return descs

if __name__ == '__main__':
    print(scrape(), len(scrape()))