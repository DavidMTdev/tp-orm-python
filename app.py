from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/production_sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Brands(db.Model):
    __tablename__ = 'brands'

    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(255))

    brand = db.relationship(
        'Products', backref=db.backref('brands', lazy=True))

    def __repr__(self):
        return '<Brands {}>'.format(self.brand_name)


class Categories(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))

    category = db.relationship(
        'Products', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return '<Categories {}>'.format(self.category_name)


class Stores(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.Integer)

    category_stocks = db.relationship(
        'Stores', backref=db.backref('stocks', lazy=True))

    category_staffs = db.relationship(
        'Stores', backref=db.backref('staffs', lazy=True))

    category_stocks = db.relationship(
        'Stores', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return '<Stores {}>'.format(self.store_name)


class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brands.brand_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.category_id'), nullable=False)
    model_year = db.Column(db.DateTime)
    list_price = product_name = db.Column(db.Float())

    product_stock = db.relationship(
        'Stocks', backref=db.backref('products', lazy=True))

    product_order_items = db.relationship(
        'Stocks', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return '<Products {}>'.format(self.product_name)


class Stocks(db.Model):
    __tablename__ = 'stocks'

    stock_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey(
        'stores.store_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.product_id'), nullable=False)
    quantity = (db.Integer)

    def __repr__(self):
        return '<Stocks {}>'.format(self.quantity)


class Customers(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    fisrt_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.Integer)

    customer = db.relationship(
        'Customers', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return '<Customers {}>'.format(self.first_name)


class Staffs(db.Model):
    __tablename__ = 'staffs'

    staff_id = db.Column(db.Integer, primary_key=True)
    fisrt_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    store_id = db.Column(db.Integer, db.ForeignKey(
        'stores.store_id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey(
        'staffs.staff_id'), nullable=False)

    staffs = db.relationship(
        'Staffs', backref=db.backref('staffs', lazy=True))

    def __repr__(self):
        return '<Staffs {}>'.format(self.first_name)


class Orders(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.customer_id'), nullable=False)
    order_status = (db.Integer)
    order_date = db.Column(db.DateTime)
    required_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)
    store_id = db.Column(db.Integer, db.ForeignKey(
        'stores.store_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staffs.staff_id'), nullable=False)

    order = db.relationship(
        'Orders', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return '<Orders {}>'.format(self.order_id)


class Order_items(db.Model):
    __tablename__ = 'order_items'

    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.product_id'), nullable=False)
    quantity = (db.Integer)
    list_price = (db.Float())
    discount = (db.Float())

    def __repr__(self):
        return '<Order_items {}>'.format(self.quantity)


@app.route('/')
def index():
    return "Hello World"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
