from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict(rules=('baked_goods',)) for bakery in bakeries]), 200


@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    return jsonify(bakery.to_dict(rules=('baked_goods',))), 200


@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([
        baked_good.to_dict(rules=('bakery',))
        for baked_good in baked_goods
    ]), 200


@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(baked_good.to_dict(rules=('bakery',))), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
