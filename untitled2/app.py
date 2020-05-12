from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
import _mysql
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/orm'
app.config['SQLALCHEMYECHO'] = True
db = SQLAlchemy(app)

with app.app_context():
    db.init_app(app)


class Brands(db.Model):
    __tablename__ = 'Brands'
    brand_id = db.Column('brand_id', db.Integer, primary_key=True)
    brand_name = db.Column('brand_name', db.VARCHAR(50))

    product = db.relationship('Products', backref='brand')

    def __repr__(self):
        return '<brands {}>'.format(self.brand_name)


class Categories(db.Model):
    __tablename__ = 'Categories'
    category_id = db.Column('category_id', db.Integer, primary_key=True)
    category_name = db.Column('category_name', db.VARCHAR(50))

    category = db.relationship('Products', backref='category')

    def __repr__(self):
        return'<categories {}>'.format(self.category_name)


class Customers(db.Model):
    __tablename__='Customers'
    customer_id = db.Column('customer_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.VARCHAR(50))
    last_name = db.Column('last_name', db.VARCHAR(50))
    phone = db.Column('phone', db.VARCHAR(10))
    email = db.Column('email', db.VARCHAR(50))
    street = db.Column('street', db.VARCHAR(100))
    city = db.Column('city', db.VARCHAR(30))
    state = db.Column('state', db.VARCHAR(30))
    zip_code = db.Column('zip_code', db.VARCHAR(10))


class Order_Items(db.Model):
    __tablename__ = 'Order_Items'
    item_id = db.Column('item_id', db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('Orders.order_id'), primary_key=True)
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('Products.product_id'))
    quantity = db.Column('quantity', db.SmallInteger)
    list_price = db.Column('list_price', db.Float)
    discount = db.Column('discount', db.Float)


class Products(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column('product_id', db.Integer, primary_key=True)
    product_name = db.Column('product_name', db.VARCHAR(50))
    brands_id = db.Column('brands_id', db.Integer, db.ForeignKey('Brands.brand_id'))
    categorys_id = db.Column('categorys_id', db.Integer, db.ForeignKey('Categories.category_id'))
    model_year = db.Column('model_year', db.DateTime, default=datetime.now())
    list_price = db.Column('list_price', db.VARCHAR(30))


class Staffs(db.Model):
    __tablename__='Staffs'
    staff_id = db.Column('staff_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.VARCHAR(50))
    last_name = db.Column('last_name', db.VARCHAR(50))
    email = db.Column('email', db.VARCHAR(50))
    phone = db.Column('phone', db.VARCHAR(10))
    active = db.Column('active', db.Boolean)
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('Stores.store_id'))
    manager_id = db.Column('manager_id', db.Integer)


stock = db.Table('Stocks',
                 db.Column('store_id', db.Integer, db.ForeignKey('Stores.store_id'), primary_key=True),
                 db.Column('product_id', db.Integer, db.ForeignKey('Products.product_id'), primary_key=True),
                 db.Column('quantity', db.SmallInteger)
                           )


class Stores(db.Model):
    __tablename__ = 'Stores'
    store_id = db.Column('store_id', db.Integer, primary_key=True)
    store_name = db.Column('store_name', db.VARCHAR(50))
    phone = db.Column('phone', db.VARCHAR(10))
    email = db.Column('email', db.VARCHAR(50))
    street = db.Column('street', db.VARCHAR(50))
    city = db.Column('city', db.VARCHAR(30))
    state = db.Column('state', db.VARCHAR(30))
    zip_code = db.Column('zip_code', db.VARCHAR(10))

    def __repr__(self):
        return '<stores {}>'.format(self.store_name)


class Orders(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column('order_id', db.Integer, primary_key=True)
    customer_id = db.Column('customer_id', db.Integer, db.ForeignKey('Customers.customer_id'))
    order_status = db.Column('order_status', db.VARCHAR(15))
    order_date = db.Column('order_date', db.DateTime, default=datetime.now)
    required_date = db.Column('required_date', db.DateTime)
    shipped_date = db.Column('shipped_date', db.DateTime)
    store_id = db.Column('store_id', db.Integer, db.ForeignKey('Stores.store_id'))
    staff_id = db.Column('staff_id', db.Integer, db.ForeignKey('Staffs.staff_id'))

from app import db
db.create_all()
#store = Stores(store_name="Test", phone="11111111", email="bob@gmail.com", street="Rue", city="Paris", state= "France", zip_code="0000")
#db.session.add(store)
#brand = Brands(brand_name="Addidas")
#category = Categories(category_name="Vetements")
#db.session.add(brand)
#db.session.add(category)
db.session.commit()

product1 = Products(product_name="Chaussures", brand="Addidas", category="Vetements", model_year="", list_price="55")
db.session.add(product1)
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)