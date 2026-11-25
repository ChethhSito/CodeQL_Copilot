const assert = require("node:assert/strict");
const test = require("node:test");
const { createApp } = require("../src/app");

function startTestServer(queryImpl) {
  const pool = { query: queryImpl };
  const app = createApp(pool);
  return new Promise((resolve) => {
    const server = app.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

test("health responde correctamente", async (t) => {
  const { server, baseUrl } = await startTestServer(async () => ({ rows: [] }));
  t.after(() => server.close());

  const response = await fetch(`${baseUrl}/health`);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { status: "ok" });
});

test("consulta productos usando el filtro recibido", async (t) => {
  let capturedArgs = [];
  const rows = [{ id: 1, name: "Teclado", category: "perifericos" }];
  const { server, baseUrl } = await startTestServer(async (...args) => {
    capturedArgs = args;
    return { rows };
  });
  t.after(() => server.close());

  const response = await fetch(`${baseUrl}/api/products?category=perifericos`);

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { products: rows });
  assert.match(capturedArgs[0], /category = \$1/);
  assert.deepEqual(capturedArgs[1], ["perifericos"]);
});
