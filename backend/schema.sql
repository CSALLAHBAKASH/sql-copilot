CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    signup_date DATE NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL
);

INSERT INTO customers (name, signup_date, country) VALUES
    ('Ava Chen', '2024-01-15', 'USA'), ('Ben Osei', '2024-02-20', 'Nigeria'),
    ('Carla Diaz', '2024-03-05', 'Mexico'), ('Dev Patel', '2024-04-10', 'India');

INSERT INTO products (name, category, price) VALUES
    ('Wireless Mouse', 'Electronics', 25.00), ('Standing Desk', 'Furniture', 350.00),
    ('Notebook', 'Office', 5.00), ('Monitor', 'Electronics', 200.00);

INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
    (1, 1, 2, '2024-05-01'), (1, 4, 1, '2024-05-15'), (2, 2, 1, '2024-05-03'),
    (3, 3, 10, '2024-05-10'), (4, 4, 2, '2024-06-01'), (2, 1, 3, '2024-06-05');