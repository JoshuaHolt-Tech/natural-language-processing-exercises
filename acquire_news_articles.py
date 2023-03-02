import os
import numpy as np
import pandas as pd
import json
from requests import get
from bs4 import BeautifulSoup
from env import *


def get_blog_articles(article_list):
    
    file = 'blog_posts.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
        
            return json.load(f)
    
    headers = {'User-Agent': 'Codeup Data Science'}
    
    article_info = []
    
    for link in article_list:
        
        response = get(link, headers=headers)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        info_dict = {'title': soup.find('h1').text,
                     'link': link,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text}
    
        article_info.append(info_dict)
        
    with open(file, 'w') as f:
        
        json.dump(article_info, f)
        
    return article_info


def scrape_one_page(topic):
    
    base_url = 'https://inshorts.com/en/read/'
    
    response = get(base_url + topic)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find_all('span', itemprop='headline')
    
    summaries = soup.find_all('div', itemprop='articleBody')
    
    summary_list = []
    
    for i in range(len(titles)):
        
        temp_dict = {'category': topic,
                     'title': titles[i].text,
                     'content': summaries[i].text}
        
        summary_list.append(temp_dict)
        
    return summary_list

def get_news_articles(topic_list):
    """
    Doesn't use topic_list if news_articles.json is in the same folder.
    """
    file = 'news_articles.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
    
    final_list = []
    
    for topic in topic_list:
        
        final_list.extend(scrape_one_page(topic))
        
    with open(file, 'w') as f:
        
        json.dump(final_list, f)
        
    return final_list

def get_article_text():
    # if we already have the data, read it locally
    if os.path.exists('article.txt'):
        with open('article.txt') as f:
            return f.read()

    # otherwise go fetch the data
    url = 'https://codeup.com/data-science/math-in-data-science/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    article = soup.find('div', id='main-content')

    # save it for next time
    with open('article.txt', 'w') as f:
        f.write(article.text)

    return article.text

def get_spam_df():
    """
    This function gets all data from the connection_logs database.
    """
    filename = "spam_db.csv"
    
    #Checks if file is catched
    if os.path.isfile(filename):
        
        df = pd.read_csv(filename)
        
        df = df.set_index('id')

        return df
    else:
        
        # read the SQL query into a dataframe
        query = """
        SELECT * FROM spam; 
        """
        
        #Gets connection to Codeup database
        df = pd.read_sql(query, get_connection('spam_db'))
        
        #Caching
        df.to_csv(filename, index=False)
        
        #Setting index
        df = df.set_index('id')

        #Return the dataframe
        return df