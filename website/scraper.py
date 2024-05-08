import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def scrape():
    page = requests.get('https://umbc.academicworks.com/')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Extracts the number of existing pages we need to scrape from
    num_pages = soup.find(class_='js-page-select')
    num_pages = len(num_pages.findAll('option'))

    scholarships = []
    for i in range(num_pages):
        page_num = i+1
        page_num = str(page_num)
        page = requests.get('https://umbc.academicworks.com/' + '?page=' + page_num)
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

        #Selects documents that students can apply for
        for i in range(len(deadlines)):
            opportunity = {'sponsor':'UMBC Academic Works', 'name':titles[i], 'gpa':0, 'status':'NP', 'hours':0, 'desc':"For more information go to " + descs[i], 'award':awards[i], 'deadline':deadlines[i]}
            scholarships.append(opportunity)

    return scholarships

def load_scholarships():
    scholarships = scrape()
    client = MongoClient(host=["mongodb://localhost:27017/"])
    db = client['FWA']
    scholarships_col = db['scholarships']

    #Remove already existing entries from the new scholarships list
    new_posts = scholarships.copy()
    for opportunity in scholarships:
        if scholarships_col.count_documents({'name' : opportunity['name']}):
            new_posts.remove(opportunity)

    #if there exists at least one new scholarship, insert it into the database
    if len(new_posts):
        scholarships_col.insert_many(new_posts)

    return

if __name__ == '__main__':
    load_scholarships()