from flask import Flask, Response

from db import create_app, db

import json



app = create_app()



class ScrapedData(db.Model):

    __tablename__ = 'scraped_data'

    id = db.Column(db.Integer, primary_key=True)

    scraped_at = db.Column(db.DateTime)

    site = db.Column(db.String)

    volume = db.Column(db.Float)

    product = db.Column(db.String)

    currency = db.Column(db.String)

    price = db.Column(db.Float)

    type = db.Column(db.String)

    category = db.Column(db.String)

    subcategory = db.Column(db.String)



@app.route('/api-matrix', strict_slashes=False)

def api_matrix():


    data = ScrapedData.query.all()

    results = [{

        "scraped_at": d.scraped_at.strftime("%Y-%m-%d %H:%M:%S") if d.scraped_at else None,

        "site": d.site,

        "volume": d.volume,

        "product": d.product,

        "currency": d.currency,

        "price": d.price,

        "type": d.type,

        "category": d.category,

        "subcategory": d.subcategory

    } for d in data]

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')



@app.route('/site/<name>')

def site_data(name):

    data = ScrapedData.query.filter_by(site=name).all()

    results = [{

        "scraped_at": d.scraped_at.strftime("%Y-%m-%d %H:%M:%S") if d.scraped_at else None,

        "site": d.site,

        "volume": d.volume,

        "product": d.product,

        "currency": d.currency,

        "price": d.price,

        "type": d.type,

        "category": d.category,

        "subcategory": d.subcategory

    } for d in data]

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')



if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(host="0.0.0.0", debug=True, port=3101)

