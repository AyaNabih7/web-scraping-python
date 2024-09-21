import requests
from bs4 import BeautifulSoup
import pandas as pd


def no_of_pages(field):
    url = 'https://wuzzuf.net/search/jobs/?a=hpb&q='+ field.replace(' ','%20')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    jobs = int(soup.find('strong').text.replace(',',''))
    pages = jobs//15
    return jobs,pages


def scrap(field):
    field = field.replace(' ','%20')
    jobs , pages = no_of_pages(field)

    titles_lst,links_lst,occupations_lst,companies_lst,campany_loc,sepcs_lst = [],[],[],[],[],[]
    for pg in range(pages):
        page = requests.get('https://wuzzuf.net/search/jobs/?q=' + field + '&start=' + str(pg))
        soup = BeautifulSoup(page.content, 'lxml')

        titles = soup.find_all('h2',{"class":"css-m604qf"})
        titles_lst += [title.text for title in titles]

        links_lst += [title.a['href'] for title in titles]

        occupations = soup.find_all('div',{"class":"css-1lh32fc"})
        occupations_lst += [occupation.text for occupation in occupations]

        companies = soup.find_all('a',{"class":"css-17s97q8"})
        companies_lst += [company.text.replace(' -','') for company in companies]

        campany_loc += soup.find_all('span',{"class":"css-5wys0k"})

        sepcs = soup.find_all('div',{'class','css-y4udm8'})
        sepcs_lst += [sepc.text for sepc in sepcs]

    scraped_data = {}
    scraped_data['Title'] = titles_lst
    scraped_data['Link'] = links_lst
    scraped_data['Occupations'] = occupations_lst
    scraped_data['Companies'] = companies_lst
    scraped_data['Company_location'] = campany_loc
    scraped_data['Sepcs'] = sepcs_lst

    data = pd.DataFrame(scraped_data)
    return data

def save_as_csv(df):
    df.to_csv('data_scraping_project.csv',index=False)
    print('Done!')