from flask import Flask, redirect, url_for, render_template
from scraper import Scraper
from opinion import Opinion
from product import Product
from flask import Response
from flask import request
import jsonpickle
from file_converter import convert_to_JSON, convert_to_CSV, convert_to_XLSX

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
            error = 'Prosze wpisac kod produktu'
        return render_template('extract.html', error = error)
    elif id in products.keys():
        return redirect(url_for('product_page', id=id))
    else:
        try:
            scraped_data = scraper.scrape_opinions(id)
        except Exception as error:
            error = str(error)
            print(error)
            if error == 'No reviews':
                return redirect(url_for('extract', error='Ten produkt nie ma zadnych opinii do pobrania'))
            elif error == 'No such page':
                return redirect(url_for('extract', error='Prosze wpisac poprawny kod produktu'))
            else:
                return redirect(url_for('extract', error='Wystąpił problem przy pobieraniu opinii'))
        
        opinions_html = scraped_data[0]
        product_info = scraped_data[1]
        opinions = []
        opinion_ids = []

        new_product = Product(id, product_info['name'], product_info['img'], product_info['num_reviews'])

        #print(opinions_html)
        for opinion in opinions_html:
            extracted_details = scraper.extract_details(opinion)
            if extracted_details['id'] not in opinion_ids:
                opinion = Opinion(extracted_details)
                opinion_ids.append(opinion.id)
                opinions.append(opinion)
            
        new_product.update_opinions(opinions)
        
        products[id] = new_product

        return redirect(url_for('product_page', id=id))

@app.route('/product/<id>')
@app.route('/product/')
def product_page(id = ''):
    if id == '':
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    else:
        return render_template('product.html', opinions = products[id].opinions, product=products[id])

@app.route('/products/')    
def product_list():
    #print(len(products))
    return render_template('product_list.html', products=products.values())

@app.route('/download/<id>')
@app.route('/download/')
def download(id='', f_type=''):
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    f_type = request.args.get('f_type', '')
    if id == '' or f_type=='':
        return redirect(url_for('product_list'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    elif f_type == 'json':
        #print(jsonpickle.encode(products[id].opinions, unpicklable=False))
        return Response(convert_to_JSON(products[id].opinions), 
            mimetype='application/json',
            headers={'Content-Disposition':f'attachment;filename=opinions-{id}.json'})
    elif f_type == 'csv':
        return Response(convert_to_CSV(products[id].opinions),
            mimetype='text/csv',
            headers={'Content-disposition':
                    f'attachment; filename=opinions-{id}.csv'})
    elif f_type == 'xlsx':
        return Response(convert_to_XLSX(products[id].opinions),
            mimetype='application/xlsx',
            headers={'Content-disposition':
                    f'attachment; filename=opinions-{id}.xlsx'})

@app.route('/charts/<id>')
@app.route('/charts/')
def charts(id=''):
    if id == '':
        return redirect(url_for('product_list'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    else:
        recommendations = {'polecam': 0, 'nie polecam': 0}
        scores = {'0.5': 0,'1.0': 0, '1.5': 0, '2.0': 0, '2.5': 0, '3.0': 0, '3.5': 0, '4.0': 0, '4.5': 0, '5.0': 0}
        for opinion in products[id].opinions:
            if opinion.recommended:
                recommendations['polecam'] += 1
            else:
                recommendations['nie polecam'] += 1
            
            score = opinion.score
            scores[str(score)] += 1
        #print(recommendations, scores)
        return render_template('charts.html', recommendations=recommendations, scores=scores, id=id)

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()

