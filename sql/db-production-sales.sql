CREATE DATABASE IF NOT EXISTS production_sales;
USE production_sales;


DROP TABLE IF EXISTS brands;
CREATE TABLE brands
(
  brand_id   INTEGER(11) NOT NULL,
  brand_name VARCHAR(255) NULL    ,
  PRIMARY KEY (brand_id)
);

DROP TABLE IF EXISTS categories;
CREATE TABLE IF NOT EXISTS categories
(
  category_id   INTEGER(11) NOT NULL,
  category_name VARCHAR(255) NULL    ,
  PRIMARY KEY (category_id)
);

DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products
(
  product_id   INTEGER(11) NOT NULL,
  product_name VARCHAR(255) NULL    ,
  list_price   FLOAT   NULL    ,
  category_id  INTEGER(11) NULL    ,
  brand_id     INTEGER(11) NULL    ,
  model_year   DATE    NULL    ,
  PRIMARY KEY (product_id)
);

DROP TABLE IF EXISTS stocks;
CREATE TABLE IF NOT EXISTS stocks
(
  product_id INTEGER(11) NOT NULL,
  store_id   INTEGER(11) NOT NULL,
  quantity   INTEGER(11) NULL    
);




DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers
(
  customer_id INTEGER(11) NOT NULL,
  first_name  VARCHAR(255) NULL    ,
  last_name   VARCHAR(255) NULL    ,
  phone       VARCHAR(255) NULL    ,
  email       VARCHAR(255) NULL    ,
  street      VARCHAR(255) NULL    ,
  city        VARCHAR(255) NULL    ,
  state       VARCHAR(255) NULL    ,
  zip_code    INTEGER(11) NULL    ,
  PRIMARY KEY (customer_id)
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE IF NOT EXISTS order_items
(
  item_id    INTEGER(11) NOT NULL,
  order_id   INTEGER(11) NULL    ,
  quantity   INTEGER(11) NULL    ,
  list_price FLOAT   NULL    ,
  discount   FLOAT   NULL    ,
  product_id INTEGER(11) NULL    ,
  PRIMARY KEY (item_id)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders
(
  order_id      INTEGER(11) NOT NULL,
  customer_id   INTEGER(11) NULL    ,
  order_status  INTEGER(11) NULL    ,
  order_date    VARCHAR(255) NULL    ,
  required_date VARCHAR(255) NULL    ,
  shipped_date  VARCHAR(255) NULL    ,
  store_id      INTEGER(11) NULL    ,
  staff_id      INTEGER(11) NULL    ,
  PRIMARY KEY (order_id)
);

DROP TABLE IF EXISTS staffs;
CREATE TABLE IF NOT EXISTS staffs
(
  staff_id   INTEGER(11) NOT NULL,
  first_name VARCHAR(255) NULL    ,
  last_name  VARCHAR(255) NULL    ,
  email      VARCHAR(255) NULL    ,
  phone      VARCHAR(255) NULL    ,
  active     INTEGER(11) NULL    ,
  store_id   INTEGER(11) NULL    ,
  manager_id INTEGER(11) NULL    ,
  PRIMARY KEY (staff_id)
);

DROP TABLE IF EXISTS stores;
CREATE TABLE IF NOT EXISTS stores
(
  store_id   INTEGER(11) NOT NULL,
  store_name VARCHAR(255) NULL    ,
  phone      VARCHAR(255) NULL    ,
  email      VARCHAR(255) NULL    ,
  street     VARCHAR(255) NULL    ,
  city       VARCHAR(255) NULL    ,
  state      VARCHAR(255) NULL    ,
  zip_code   INTEGER(11) NULL    ,
  PRIMARY KEY (store_id)
);





ALTER TABLE orders
  ADD CONSTRAINT FK_customers_TO_orders
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id);

ALTER TABLE orders
  ADD CONSTRAINT FK_stores_TO_orders
    FOREIGN KEY (store_id)
    REFERENCES stores (store_id);

ALTER TABLE orders
  ADD CONSTRAINT FK_staffs_TO_orders
    FOREIGN KEY (staff_id)
    REFERENCES staffs (staff_id);

ALTER TABLE staffs
  ADD CONSTRAINT FK_stores_TO_staffs
    FOREIGN KEY (store_id)
    REFERENCES stores (store_id);

ALTER TABLE order_items
  ADD CONSTRAINT FK_orders_TO_order_items
    FOREIGN KEY (order_id)
    REFERENCES orders (order_id);

ALTER TABLE products
  ADD CONSTRAINT FK_categories_TO_products
    FOREIGN KEY (category_id)
    REFERENCES categories (category_id);

ALTER TABLE order_items
  ADD CONSTRAINT FK_products_TO_order_items
    FOREIGN KEY (product_id)
    REFERENCES products (product_id);

ALTER TABLE stocks
  ADD CONSTRAINT FK_products_TO_stocks
    FOREIGN KEY (product_id)
    REFERENCES products (product_id);

ALTER TABLE stocks
  ADD CONSTRAINT FK_stores_TO_stocks
    FOREIGN KEY (store_id)
    REFERENCES sales.stores (store_id);

ALTER TABLE products
  ADD CONSTRAINT FK_brands_TO_products
    FOREIGN KEY (brand_id)
    REFERENCES brands (brand_id);

      