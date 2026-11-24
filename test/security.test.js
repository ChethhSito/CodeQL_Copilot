const assert = require("node:assert/strict");
const test = require("node:test");
const { createApp } = require("../src/app");

test("prueba esperada después de Autofix: usa SQL parametrizado", async (t) => {
  let captured = null;
  const pool = {
    query: async (...args) => {
      captured = args;
      return { rows: [] };
    },
  };
  const app = createApp(pool);
  const server = app.listen(0, "127.0.0.1");
  t.after(() => server.close());

  await new Promise((resolve) => server.once("listening", resolve));
  const { port } = server.address();
  const payload = "' OR '1'='1";
  await fetch(
    `http://127.0.0.1:${port}/api/products?category=${encodeURIComponent(payload)}`,
  );

  assert.equal(captured.length, 2, "pool.query debe recibir SQL y parámetros");
  assert.match(captured[0], /\$1/);
  assert.deepEqual(captured[1], [payload]);
});
