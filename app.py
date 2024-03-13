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
    elif id in products.keys():
        print('bez dodatkowego pobierania')
        return render_template('extract.html', opinions = products[id].opinions, product = products[id])
    else:
        try:
            scraped_data = scraper.scrape_opinions(id)
        except Exception as error:
            print(error)
            return '<h1>error</h1>'
        opinions_html = scraped_data[0]
        product_info = scraped_data[1]
        opinions = []

        new_product = Product(id, product_info['name'], product_info['img'], product_info['num_reviews'])

        print(opinions_html)
        for opinion in opinions_html:
            extracted_details = scraper.extract_details(opinion)
            opinion = Opinion(extracted_details)
            opinions.append(opinion)
        
        new_product.set_opinions(opinions)
        
        products[id] = new_product

        return render_template('extract.html', opinions = new_product.opinions, product = new_product)

@app.route('/product/')
@app.route('/product/<id>')
def product_page(id):
    if id == '':
        return '<h1>Prosze wprowadzic prawidlowy kod produktu</h1>'
    elif id != '' and id not in products.keys():
        return '<h1>Prosze najpierw pobrac opinie tego produktu</h1>'
    else:
        return '<h1>amogu</h1>'
        
if __name__ == '__main__':
    app.run()

