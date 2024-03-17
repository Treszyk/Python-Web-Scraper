from flask import Flask, redirect, url_for, render_template
from scraper import Scraper
from opinion import Opinion
from product import Product
import openpyxl
import io
import csv
from flask import Response
from flask import request
import jsonpickle

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
        
        new_product.update_opinions(opinions)
        
        products[id] = new_product

        return redirect(url_for('product_page', id=id))#('extract.html', opinions = new_product.opinions, product = new_product)

@app.route('/product/<id>')
@app.route('/product/')
def product_page(id = ''):
    if id == '':
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))#'<h1>Prosze najpierw pobrac opinie tego produktu</h1>'
    else:
        return render_template('product.html', opinions = products[id].opinions, product=products[id])

@app.route('/products/')    
def product_list():
    print(len(products))
    return render_template('product_list.html', products=products.values())

#add a safeguard if an id is entered but its not in products
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
        print(jsonpickle.encode(products[id].opinions, unpicklable=False))
        #print(json.dump(products[id]))
        return Response(jsonpickle.encode(products[id].opinions, unpicklable=False), 
            mimetype='application/json',
            headers={'Content-Disposition':f'attachment;filename=opinions-{id}.json'})
    elif f_type == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "author", "recommended", "score", "verified", "review_date", "buy_date", "likes", "dislikes", "content", "plus", "minus"])
        for opinion in products[id].opinions:
            writer.writerow(opinion.serialize())
        output_val = output.getvalue()
        output.close()
        return Response(output_val,
            mimetype="text/csv",
            headers={"Content-disposition":
                    f"attachment; filename=opinions-{id}.csv"})
    elif f_type == 'xlsx':
        output = io.BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["id", "author", "recommended", "score", "verified", "review_date", "buy_date", "likes", "dislikes", "content", "plus", "minus"])
        for opinion in products[id].opinions:
            sheet.append(opinion.serialize()) 
        workbook.save(output)   
        output_val = output.getvalue()
        output.close() 
        return Response(output_val,
            mimetype="application/xlsx",
            headers={"Content-disposition":
                    "attachment; filename=opinions-{id}.xlsx"})

@app.route('/charts/<id>')
@app.route('/charts/')
def charts(id=''):
    if id == '':
        return redirect(url_for('product_list'))
    elif id != '' and id not in products.keys():
        return redirect(url_for('extract', error='Prosze najpierw pobrac opinie tego produktu'))
    else:
        #kołowy podział poszczególnych rekomendacji w ogólnej liczbie opinii [czyli ze polecam nie polecam]
        #słupkowy lub kolumnowy przedstawiajacy liczbe opinii z poszczegolnymi liczbami gwiazdek
        recommendations = {'polecam': 0, 'nie polecam': 0}
        scores = {'1.0': 0, '1.5': 0, '2.0': 0, '2.5': 0, '3.0': 0, '3.5': 0, '4.0': 0, '4.5': 0, '5.0': 0}
        for opinion in products[id].opinions:
            if opinion.recommended:
                recommendations['polecam'] += 1
            else:
                recommendations['nie polecam'] += 1
            
            score = opinion.score
            scores[str(score)] += 1
        print(recommendations, scores)

        return render_template('charts.html', recommendations=recommendations, scores=scores, id=id)

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()

