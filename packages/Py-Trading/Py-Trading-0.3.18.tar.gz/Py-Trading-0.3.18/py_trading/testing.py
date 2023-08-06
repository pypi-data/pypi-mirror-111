from requests import get 
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
from pathlib import Path
import pandas as pd
from GoogleNews import GoogleNews

def testing():
    sectors = ['Taiwan', 'Semiconductors', 'Technology']
    sector_news = []
    if sectors:
        for sector in sectors:
            googlenews = GoogleNews(lang='en', period='14d')
            googlenews.get_news(sector)
            sector_news.append(googlenews.result())
            
                
    print(sector_news)
    
testing()

# googlenews = GoogleNews(lang='en', period='14d') # Specify period for news
# googlenews.get_news('Semiconductors')
# print(googlenews.result()['title'])
