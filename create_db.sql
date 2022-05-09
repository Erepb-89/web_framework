
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS buyer;
CREATE TABLE buyer (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
INSERT INTO buyer (id, name) VALUES (0, 'Andrey');
INSERT INTO buyer (id, name) VALUES (1, 'Ilya');
INSERT INTO buyer (id, name) VALUES (2, 'Evgeniy');
INSERT INTO buyer (id, name) VALUES (3, 'Petr');

DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32));
INSERT INTO category (id, name) VALUES (0, 'стулья');
INSERT INTO category (id, name) VALUES (1, 'столы');
INSERT INTO category (id, name) VALUES (2, 'кресла');
INSERT INTO category (id, name) VALUES (3, 'диваны');

DROP TABLE IF EXISTS product;
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    category INTEGER,
    price INTEGER);
INSERT INTO product (id, name, category, price) VALUES (0, 'красивый стул1', 0, 6000);
INSERT INTO product (id, name, category, price) VALUES (1, 'красивый стул2', 0, 7000);
INSERT INTO product (id, name, category, price) VALUES (2, 'обычный стул', 0, 4000);
INSERT INTO product (id, name, category, price) VALUES (3, 'красивый стол', 1, 30000);
INSERT INTO product (id, name, category, price) VALUES (4, 'обычный стол', 1, 15000);
INSERT INTO product (id, name, category, price) VALUES (5, 'красивое кресло', 2, 15000);
INSERT INTO product (id, name, category, price) VALUES (6, 'обычное кресло', 2, 10000);
INSERT INTO product (id, name, category, price) VALUES (7, 'красивый диван', 3, 50000);
INSERT INTO product (id, name, category, price) VALUES (8, 'обычный диван', 3, 25000);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
