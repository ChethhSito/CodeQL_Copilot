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

test("documenta la propagación de la entrada dentro del SQL vulnerable", async (t) => {
  let capturedSql = "";
  const { server, baseUrl } = await startTestServer(async (sql) => {
    capturedSql = sql;
    return { rows: [] };
  });
  t.after(() => server.close());

  const payload = "' OR '1'='1";
  const response = await fetch(
    `${baseUrl}/api/products?category=${encodeURIComponent(payload)}`,
  );

  assert.equal(response.status, 200);
  assert.match(capturedSql, /OR '1'='1/);
});
