from bs4 import BeautifulSoup
import math
import requests
from opinion import Opinion

class Scraper:
    def __init__(self):
        pass
        
    def scrape_opinions(self, id:str) -> tuple:
        reviews = []
        product_info = {}
        re = requests.get(f'https://www.ceneo.pl/{id}/opinie-{1}')
        soup = BeautifulSoup(re.text, 'html.parser')
        
        if soup.find('div', class_='error-page') or soup.find('h1', {"title" : "Błąd 500"}, class_='title'):
            raise Exception("No such page")

        for review in soup.find_all('div', class_='user-post user-post__card js_product-review'):
            reviews.append(review)

        reviews_li = soup.find('li', class_ = 'page-tab reviews')
        reviews_span = reviews_li.find('span')

        number_of_reviews = int(reviews_span.text.replace('Opinie i Recenzje (', '').replace(')', ''))
        #number_of_reviews = min(number_of_reviews, 100)

        product_info['name'] = soup.find('h1', class_ = 'product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor').text
        product_info['img'] = soup.find('img', class_='js_gallery-media gallery-carousel__media')['src']
        product_info['num_reviews'] = number_of_reviews

        for i in range(2, math.ceil(number_of_reviews/10)+1):
            re = requests.get(f'https://www.ceneo.pl/{id}/opinie-{i}')
            soup = BeautifulSoup(re.text, 'html')
            for review in soup.find_all('div', class_='user-post user-post__card js_product-review'):
                reviews.append(review)

        return (reviews, product_info)

    def extract_details(self, opinion) -> Opinion:
        #id:str, author:str, recommended:bool, score:int, verified:bool, review_date:str, buy_date:str, likes:int, dislikes:int, content:str, plus:list[str], minus:list[str]
        id = opinion['data-entry-id']
        author = opinion.find('span', class_='user-post__author-name').text

        recommend_div = opinion.find('span', class_='user-post__author-recomendation')
        recommended = ''
        if recommend_div:
            recommended = True if recommend_div.find('em').text == 'Polecam' else False

        score = float(opinion.find('span', class_='user-post__score-count').text.replace(',', '.').split('/')[0])
        verified = True if opinion.find('div', 'review-pz') else False

        dates = opinion.find('span', class_='user-post__published').find_all('time')
        review_date = dates[0]['datetime'] if len(dates) >= 1 else ''
        buy_date = dates[1]['datetime'] if len(dates) >= 2 else '' 

        likes = int(opinion.find('button', class_='vote-yes js_product-review-vote js_vote-yes').find('span').text)
        dislikes = int(opinion.find('button', class_='vote-no js_product-review-vote js_vote-no').find('span').text)
        content = opinion.find('div', class_='user-post__text').text

        plus = []
        minus = []
        plus_minus = opinion.find_all('div', class_='review-feature__col')

        for div in plus_minus:
            print(div.find('div', class_='review-feature__title'))
            if div.find('div', class_='review-feature__title').text == 'Zalety':
                for val in div.find_all('div', class_='review-feature__item'):
                    plus.append(val.text)
            else:
                for val in div.find_all('div', class_='review-feature__item'):
                    minus.append(val.text)
         
        return {'id': id, 'author': author, 'recommended': recommended, 'score': score, 'verified': verified, 'review_date': review_date, 'buy_date': buy_date, 'likes': likes, 'dislikes': dislikes, 'content': content, 'plus': plus, 'minus': minus}
