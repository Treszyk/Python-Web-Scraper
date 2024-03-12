from bs4 import BeautifulSoup
import math
import requests

class Scraper:
    def __init__(self):
        pass
        
    def scrape_opinions(self, id:str) -> list:
        reviews = []
        #first page + number of reviews
        re = requests.get(f'https://www.ceneo.pl/{id}/opinie-{1}')
        soup = BeautifulSoup(re.text, 'html')

        for review in soup.find_all('div', class_='user-post user-post__card js_product-review'):
            reviews.append(review)

        reviews_li = soup.find('li', class_ = 'page-tab reviews')
        reviews_span = reviews_li.find('span')

        #print(f'number of reviews {reviews_span.text} {reviews_span.text.replace('Opinie i Recenzje (', '').replace(')', '')}')
        number_of_reviews = int(reviews_span.text.replace('Opinie i Recenzje (', '').replace(')', ''))
        if number_of_reviews > 40:
            return reviews
        #Opinie i Recenzje (18)
        #getting the reviews from all pages
        for i in range(2, math.ceil(number_of_reviews/10)+1):
            re = requests.get(f'https://www.ceneo.pl/{id}/opinie-{i}')
            #print(re.text, math.ceil(number_of_reviews/10)+1)
            soup = BeautifulSoup(re.text, 'html')
            for review in soup.find_all('div', class_='user-post user-post__card js_product-review'):
                reviews.append(review)
        #print(len(reviews), reviews[0])
        return reviews

    def extract_details(self, opinion) -> dict:
        #id:str, author:str, recommended:bool, score:int, verified:bool, review_date:str, buy_date:str, likes:int, dislikes:int, content:str, plus:int, minus:int
        pass
