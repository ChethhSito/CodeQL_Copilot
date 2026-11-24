# Laboratorio CodeQL y Copilot Autofix

Proyecto del grupo 3 para demostrar detección semántica, una consulta QL propia,
remediación asistida y un pipeline combinado con Semgrep.

> **Advertencia académica:** `src/app.js` contiene vulnerabilidades intencionales.
> Ejecute el proyecto solo en un entorno local y autorizado. No lo despliegue en
> Internet ni reutilice el código vulnerable en producción.

El servidor escucha únicamente en `127.0.0.1`. El caso de `eval` permanece
deshabilitado salvo que `ENABLE_EVAL_LAB=true`; no es necesario habilitarlo para
que CodeQL y Semgrep lo detecten.

## Objetivos demostrables

- Detectar SQL injection con una consulta estándar de CodeQL.
- Visualizar el flujo desde una entrada HTTP hasta una operación de base de datos.
- Revisar una propuesta de Copilot Autofix y comprobarla con una prueba.
- Ejecutar una consulta QL creada por el grupo.
- Publicar hallazgos de Semgrep junto con CodeQL mediante SARIF.

## Requisitos

- Node.js 20 o superior.
- Git y una cuenta de GitHub con permiso para configurar Actions.
- Docker, solo si se desea levantar PostgreSQL para la demostración interactiva.
- Un repositorio público, o GitHub Code Security habilitado si es privado.

## Ejecución local

```bash
npm install
npm test
```

La prueba funcional confirma que el dato controlado por el usuario llega al SQL.
La prueba de seguridad representa el criterio de aceptación del parche:

```bash
npm run test:security
```

En la versión inicial debe fallar. Después de parametrizar la consulta debe pasar.

Para levantar la aplicación con PostgreSQL:

```bash
docker compose up -d
npm start
```

Prueba funcional sin carga ofensiva:

```bash
curl "http://localhost:3000/api/products?category=perifericos"
```

## Activación en GitHub

1. Cree un repositorio público vacío y suba este contenido a `main`.
2. Abra **Actions** y habilite los workflows si GitHub lo solicita.
3. Espere las ejecuciones **CodeQL** y **Semgrep**.
4. Abra **Security > Code scanning** para revisar resultados.
5. En una alerta estándar compatible, seleccione la opción para generar una
   corrección con Copilot Autofix.
6. Revise el parche en una rama o pull request.
7. Ejecute `npm test` y `npm run test:security`.
8. Confirme mediante un nuevo análisis que la alerta desaparece.

Copilot Autofix no genera una corrección para toda alerta y no debe demostrarse
con la consulta personalizada. Use una alerta estándar compatible y verifique la
opción antes de la exposición.

## Corrección esperada para revisar el Autofix

El cambio seguro debe conservar `category` fuera del texto SQL:

```javascript
const sql =
  "SELECT id, name, category, price FROM products WHERE category = $1 ORDER BY name";
const result = await pool.query(sql, [category]);
```

No aplique este cambio antes de obtener la evidencia inicial, porque eliminaría
la vulnerabilidad que necesita detectar la primera ejecución.

## Documentación del proyecto

- [Arquitectura](docs/ARQUITECTURA.md)
- [Guía de demo](docs/GUIA_DEMO.md)
- [Base del informe](docs/INFORME_BASE.md)

## Evidencias que debe guardar el grupo

- URL y commit del análisis.
- Ejecuciones completas de ambos workflows.
- Alerta CodeQL con recorrido de datos.
- Resultado de la consulta QL propia.
- Sugerencia original de Copilot Autofix y diff aplicado.
- Pruebas antes y después de la corrección.
- Segundo análisis sin la alerta corregida.
- Duración y número de hallazgos de cada herramienta.

Las cifras del informe deben provenir de estas ejecuciones; no complete resultados
con valores inventados.
