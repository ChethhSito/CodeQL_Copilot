CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(50) NOT NULL,
  price NUMERIC(10, 2) NOT NULL
);

INSERT INTO products (name, category, price) VALUES
  ('Teclado', 'perifericos', 120.00),
  ('Mouse', 'perifericos', 65.00),
  ('Monitor', 'pantallas', 850.00);
