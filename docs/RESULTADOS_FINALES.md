# Resultados finales del laboratorio

Fecha de medición: 25 de noviembre de 2026.

## Ejecuciones

| Etapa | Workflow | Run ID | Commit | Duración | Resultado |
|---|---|---:|---|---:|---|
| Inicial | CodeQL | 45657346922 | 83cdc22 | 96 s | Éxito |
| Inicial | Semgrep | 45657347138 | 83cdc22 | 38 s | Éxito |
| Pull request final | CodeQL | 45673902770 | 17b8f96 | 69 s | Éxito |
| Final en main | CodeQL | 45674463710 | 8dd28ee | 93 s | Éxito |
| Final en main | Semgrep | 45674463631 | 8dd28ee | 25 s | Éxito |

Los tiempos corresponden a la duración completa de cada job en GitHub Actions.
Son observaciones del laboratorio y no constituyen un benchmark general.

## Hallazgos

| Hallazgo | Herramienta | Estado final |
|---|---|---|
| Database query built from user-controlled sources | CodeQL | Corregido |
| grupo3.javascript.sql-concatenado | Semgrep | Corregido |
| Missing rate limiting | CodeQL | Corregido |
| Uso de eval en JavaScript | CodeQL personalizado | Abierto por diseño |
| Code injection | CodeQL estándar | Abierto por diseño |
| grupo3.javascript.eval | Semgrep | Abierto por diseño |

## Validación

- Dos pruebas funcionales aprobadas.
- Una prueba de seguridad aprobada.
- Cero vulnerabilidades reportadas por npm audit.
- Pull request 1 fusionado en `main`.
- CodeQL y Semgrep finalizaron correctamente después de la fusión.

## Enlaces reproducibles

- Repositorio: https://github.com/ChethhSito/CodeQL_Copilot
- Pull request: https://github.com/ChethhSito/CodeQL_Copilot/pull/1
- CodeQL final: https://github.com/ChethhSito/CodeQL_Copilot/actions/runs/45674463710
- Semgrep final: https://github.com/ChethhSito/CodeQL_Copilot/actions/runs/45674463631
