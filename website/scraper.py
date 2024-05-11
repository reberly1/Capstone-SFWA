"""
Websites Referenced:
[13] https://brightdata.com/blog/how-tos/web-scraping-with-python
[14] https://umbc.academicworks.com/
"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

#Change this string to match your mongodb server host
HOST = "mongodb://localhost:27017/"

def scrape():
    """
    Description
    Scrapes all scholarships off of academic works

    Parameters
    None

    Returns       None
    """
    page = requests.get('https://umbc.academicworks.com/')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Extracts the number of existing pages we need to scrape from
    num_pages = soup.find(class_='js-page-select')
    num_pages = len(num_pages.findAll('option'))

    scholarships = []
    #For each page on academic works, scrape all scholarship data
    for i in range(num_pages):
        page_num = i+1
        page_num = str(page_num)
        page = requests.get('https://umbc.academicworks.com/' + '?page=' + page_num)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        #Extracts the table where all scholarship data is located
        table = soup.find(class_='full striped-table')
        
        #Extracts scholarship titles
        titles = []
        name_href = table.find_all('a')
        for href in name_href:
            titles.append(href.get_text(strip=True))

        #Extracts the url for the scholarship
        descs = []
        desc_row = table.find_all('a')
        for desc in desc_row:
            href = desc.get('href')
            descs.append("https://umbc.academicworks.com" + href)

        #Extracts the scholarship reward
        awards = []
        award_row = table.find_all(class_='strong h4 table__column--max-width-250')
        for row in award_row:
            awards.append(row.get_text(strip=True))

        #Extracts the scholarship deadline
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
    """
    Description
    Uploads all scraped scholarships to mongodb

    Parameters
    None

    Returns       None
    """
    scholarships = scrape()
    client = MongoClient(host=[HOST])
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