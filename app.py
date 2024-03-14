from flask import Flask, redirect, url_for, render_template
from scraper import Scraper
from opinion import Opinion
from product import Product
from flask import request

app = Flask(__name__)
products = {}
scraper = Scraper()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/extract/', methods=['GET'])
def extract(id='', error=''):
    id = request.args.get('id', '')
    error = request.args.get('error', '')
    submitted = True if request.args.get('form_submitted') == 'true' else False
    print(id)
    if id == '':
        if submitted:
            error = 'Prosze wpisac poprawny kod!'
        return render_template('extract.html', error = error)
    elif id in products.keys():
        print('bez dodatkowego pobierania')
        return redirect(url_for('product_page', id=id))#('extract.html', opinions = products[id].opinions, product = products[id])
    else:
        try:
            scraped_data = scraper.scrape_opinions(id)
        except Exception as error:
            print(error)
            return redirect(url_for('extract', error='Prosze wpisac poprawny kod'))
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

        return redirect(url_for('product_page', id=id))#('extract.html', opinions = new_product.opinions, product = new_product)

@app.route('/product/')
@app.route('/product/<id>')
def product_page(id):
    if id == '':
        return redirect(url_for('extract'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))#'<h1>Prosze najpierw pobrac opinie tego produktu</h1>'
    else:
        return render_template('product.html', opinions = products[id].opinions, product=products[id])
        
if __name__ == '__main__':
    app.run()

