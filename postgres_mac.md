
# Install PostgreSQL (installs latest version)
```
brew install postgresql
```

# Start the PostgreSQL background service
```
brew services start postgresql
```

# Connect to the default database using the CLI tool
```
psql postgres
```

```
-- 1. Create a new database
CREATE DATABASE company_db;

-- 2. Connect to the new database
\c company_db;

-- 3. Create a table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    salary NUMERIC
);


-- Insert a single row
INSERT INTO employees (name, role, salary) 
VALUES ('Alice Smith', 'Software Engineer', 95000);

-- Insert multiple rows at once
INSERT INTO employees (name, role, salary) 
VALUES 
    ('Bob Jones', 'Data Scientist', 105000),
    ('Charlie Brown', 'Product Manager', 90000);

-- View the inserted data
SELECT * FROM employees;
```


4. Useful CLI Commands
```
• \l : List all databases
• \dt : List all tables in the current database
• \d table_name : Describe a table's schema (columns and data types)
• \q : Exit the psql CLI
```




```
createdb mydb
psql mydb
-- Step A: Create a sample table and add data
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT
);

INSERT INTO orders (item_name, quantity) VALUES 
('Laptop', 1),
('Monitor', 2);

-- Step B: Create the read-only role (From your image)
CREATE ROLE readonly_app WITH LOGIN PASSWORD 'testpassword123';

-- Step C: Grant read-only permissions (Targeting mydb)
GRANT CONNECT ON DATABASE mydb TO readonly_app;
GRANT USAGE ON SCHEMA public TO readonly_app;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_app;

psql "postgresql://readonly_app:testpassword123@localhost:5432/mydb" -c "SELECT * FROM orders;"
psql "postgresql://readonly_app:testpassword123@localhost:5432/mydb" -c "DELETE FROM orders WHERE id = 1;"

```

```
READONLY_DATABASE_URL=postgresql://readonly_app:postgres@localhost/mydb
psql "$READONLY_DATABASE_URL" -c "DELETE FROM orders WHERE id = 1;"

```