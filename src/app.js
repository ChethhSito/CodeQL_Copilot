const express = require("express");

/**
 * Crea la aplicación con una conexión inyectable para poder probar el flujo
 * sin depender de una base de datos real.
 */
function createApp(pool) {
  const app = express();
  app.use(express.json());

  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  // LABORATORIO VULNERABLE: concatenar entrada externa permite SQL injection.
  app.get("/api/products", async (req, res, next) => {
    try {
      const category = req.query.category || "general";
      const sql =
        "SELECT id, name, category, price FROM products WHERE category = $1 ORDER BY name";

      const result = await pool.query(sql, [category]);
      res.json({ products: result.rows });
    } catch (error) {
      next(error);
    }
  });

  // LABORATORIO VULNERABLE: caso simple para la consulta QL creada por el grupo.
  app.get("/api/evaluate", (req, res) => {
    if (process.env.ENABLE_EVAL_LAB !== "true") {
      return res.status(404).json({ error: "Caso eval deshabilitado" });
    }

    const expression = String(req.query.expression || "0");
    const result = eval(expression);
    res.json({ result });
  });

  app.use((error, _req, res, _next) => {
    res.status(500).json({ error: "Error interno del laboratorio" });
  });

  return app;
}

module.exports = { createApp };
