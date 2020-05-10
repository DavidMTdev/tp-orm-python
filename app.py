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

    product = db.relationship('Products', backref='brand')

    def __repr__(self):
        return '<Brands {}>'.format(self.brand_name)

class Categories(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))

    category = db.relationship('Products', backref='category')

    def __repr__(self):
        return '<Categories {}>'.format(self.category_name)

stock = db.Table('stocks',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.store_id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'), primary_key=True),
    db.Column('quantity', db.Integer)
)

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

    category_stocks = db.relationship('Products', secondary=stock, backref=db.backref('contains', lazy='dynamic'))

    category_staffs = db.relationship('Staffs', backref='staff')

    category_orders = db.relationship('Orders', backref='store')

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
    list_price = db.Column(db.Float())

    product_order_items = db.relationship('Order_items', backref='product')

    def __repr__(self):
        return '<Products {}>'.format(self.product_name)

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

    customer = db.relationship('Orders', backref='customer')

    def __repr__(self):
        return '<Customers {}>'.format(self.first_name)

class Staffs(db.Model):
    __tablename__ = 'staffs'

    staff_id = db.Column(db.Integer, primary_key=True)
    fisrt_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    store_id = db.Column(db.Integer, db.ForeignKey(
        'stores.store_id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey(
        'staffs.staff_id'))

    staffs = db.relationship('Staffs', remote_side=[staff_id], backref=db.backref('manage', uselist=False)) #uselist=False pour les relation OneToOne evite une erreur
    # remote_side permet de faire un OneToOne

    staffs_orders = db.relationship('Orders', backref='staff')

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

    order = db.relationship('Order_items', backref='order')

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
    brand = Brands(brand_name="louis")
    db.session.add(brand)

    category = Categories(category_name="sport")
    db.session.add(category)

    store = Stores(store_name="decathlon", phone="0613922847", email="blabla@gmail.com", street="54 rue de messi", city="Paris", state="Français", zip_code=95700)
    db.session.add(store)

    product = Products(product_name="produit", brand=brand, category=category, model_year='2019-01-16 00:00:00', list_price=29.99)
    db.session.add(product)

    product.contains.append(store)

    customer = Customers(fisrt_name="blibli", last_name="gagaga", phone="0613922847", email="blabla@gmail.com", street="54 rue de messi", city="Paris", state="Français", zip_code=95700)
    db.session.add(customer)

    staff = Staffs(fisrt_name="blibli", last_name="gagaga", phone="0613922847", email="blabla@gmail.com", active=True, staff=store, manage=None)
    db.session.add(staff)

    order = Orders(customer=customer, order_status=1, order_date='2019-01-16 00:00:00', required_date='2019-01-16 00:00:00', shipped_date='2019-01-16 00:00:00', store=store, staff=staff)
    db.session.add(order)

    order_item = Order_items(order=order, product=product, quantity=22, list_price=10, discount=5)
    db.session.add(order_item)

    db.session.commit()
    return "Hello World"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
