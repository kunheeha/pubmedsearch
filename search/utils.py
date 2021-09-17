from .models import Search, Article, Link
import requests
from bs4 import BeautifulSoup

def obtain_article_links(search):
    # Scraping all links to first 10 articles
    source = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={search}').text
    soup = BeautifulSoup(source, 'lxml')
    articles = soup.find_all('article', class_='full-docsum')
    article_links=[]
    for article in articles:
        article_links.append(article.a.get('href'))

    return article_links

def create_article_object(link, search_folder):
    pubmedlink = f'https://pubmed.ncbi.nlm.nih.gov/{link}'
    source = requests.get(pubmedlink).text
    soup = BeautifulSoup(source, 'lxml')
    title = soup.find('h1', class_='heading-title').get_text().strip()
    # Try Except because some may not have an abstract
    try:
        abstract_div = soup.find('div', class_='abstract-content')
        abstract = abstract_div.p.get_text()
        abstract.replace('\n', '')
    except:
        abstract = "No abstract"

    scraped_article = Article(title=title, abstract=abstract, pubmedlink=pubmedlink, search_folder=search_folder)
    scraped_article.save()

    return scraped_article, pubmedlink
    
def create_link_object(article, link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    try:
        free_text = soup.find('span', class_='free-label').get_text()
        if 'free' in free_text or 'Free' in free_text:
            free = True
        else:
            free = False
    except:
        free = False
    full_texts_list = []
    full_text_links = soup.find('div', class_='full-text-links-list')
    for link in full_text_links.find_all('a'):
        full_texts_list.append(link.get('href'))

    for link in full_texts_list:
        Link(link=link, free=free, article=article).save()


