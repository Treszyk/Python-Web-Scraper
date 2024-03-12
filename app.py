from flask import Flask, redirect, url_for, render_template
from scraper import Scraper
from opinion import Opinion
from product import Product

app = Flask(__name__)
products = {}
scraper = Scraper()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/extract/')
@app.route('/extract/<id>')
def extract(id='', error=''):
    print(id)
    if id == '':
        return '<h1>extract_menu</h1>'
    else:
        #opinions = scraper.scrape_opinions('145964652')
        #print(opinions)
        return f'<h1>extracting {id}... and then redirect to product page if the id is valid else redirect to extract with an error </h1>'
    
if __name__ == '__main__':
    app.run()

