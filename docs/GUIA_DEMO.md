# Guía de demostración

Duración objetivo: 15 minutos.

## Preparación previa

1. Use un repositorio público de GitHub para evitar depender de una licencia de
   GitHub Code Security para un repositorio privado.
2. Suba el proyecto a la rama `main` y confirme que ambos workflows terminan.
3. Verifique las alertas en **Security > Code scanning**.
4. Confirme antes de la exposición que la alerta estándar elegida ofrece
   **Generate fix**. Copilot Autofix no garantiza una sugerencia para toda alerta.
5. Prepare una rama o pull request para aplicar y revisar la corrección.
6. Grabe un video de respaldo cuando el flujo funcione de principio a fin.

## Guion cronometrado

### 0:00 a 2:00 — Problema y arquitectura

- Explique SAST semántico y la idea de código como datos.
- Muestre `docs/ARQUITECTURA.md`.
- Aclare que todo ocurre en un laboratorio autorizado.

### 2:00 a 5:00 — Código vulnerable

- Abra `src/app.js`.
- Siga `req.query.category` hasta `pool.query`.
- Ejecute `npm test` para mostrar que la aplicación funciona.
- Ejecute `npm run test:security`; al inicio debe fallar porque el SQL todavía no
  está parametrizado.

### 5:00 a 8:00 — CodeQL

- Abra la ejecución de GitHub Actions.
- Muestre la alerta estándar de SQL injection y su recorrido de datos.
- Explique fuente, propagación y sumidero.

### 8:00 a 11:00 — Copilot Autofix

- Genere o abra la corrección sugerida.
- Revise que use un marcador `$1` y el arreglo `[category]`.
- No acepte el cambio solo porque fue generado por IA; compare el parche con la
  recomendación técnica y ejecute las pruebas.

### 11:00 a 13:00 — Consulta propia

- Abra `codeql/DangerousEval.ql`.
- Explique metadatos, `from`, `where` y `select`.
- Muestre su alerta separada en Code scanning.

### 13:00 a 15:00 — Semgrep y conclusión

- Muestre el workflow de Semgrep y las alertas sobre el mismo commit.
- Compare duración, tipo de análisis y contexto mostrado.
- Termine con el nuevo análisis del parche y la prueba de seguridad aprobada.

## Plan de contingencia

Si GitHub o Autofix no responde durante la exposición, use el video de respaldo
y las capturas del último workflow exitoso. No simule que una corrección manual
fue producida por Autofix: indique claramente qué parte es evidencia grabada.
