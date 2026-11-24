const { Pool } = require("pg");
const { createApp } = require("./app");

const port = Number(process.env.PORT || 3000);
const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    "postgresql://lab_user:lab_password@localhost:5432/codeql_lab",
});

const app = createApp(pool);

app.listen(port, "127.0.0.1", () => {
  console.log(`Laboratorio disponible en http://localhost:${port}`);
});
