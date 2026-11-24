# Estructura de la presentación

Propuesta para 30 a 35 minutos de exposición, seguida por 15 minutos de demo.

## Diapositivas

1. **Título e integrantes** — proyecto, curso y roles.
2. **Problema** — vulnerabilidades que llegan al repositorio y límites de la
   revisión manual.
3. **Objetivos y alcance** — detección, remediación, consulta propia y comparación.
4. **Qué es SAST** — momento de ejecución, fortalezas y limitaciones.
5. **Arquitectura de CodeQL** — extracción, base de datos y consultas.
6. **Flujo de datos** — fuente, propagación, barreras y sumidero.
7. **Lenguaje QL** — estructura mínima de una consulta.
8. **Caso SQL injection** — CWE-89 y código del laboratorio.
9. **Consulta creada por el grupo** — metadatos, `from`, `where` y `select`.
10. **Copilot Autofix** — entrada, sugerencia, revisión y validación.
11. **Riesgos de una corrección generada** — errores funcionales, cambios parciales
    y necesidad de pruebas.
12. **Integración CI/CD** — workflows de CodeQL y Semgrep.
13. **Comparación experimental** — tabla con tiempos y hallazgos reales.
14. **Resultados antes y después** — alerta, parche, prueba y nuevo análisis.
15. **Limitaciones y conclusiones** — alcance de la muestra y aprendizajes.
16. **Preguntas** — repositorio y referencias.

## Reparto para cinco integrantes

| Rol | Responsabilidad principal |
|---|---|
| Coordinación | Introducción, objetivos, integración y control del tiempo |
| CodeQL | Arquitectura, flujo de datos y workflow |
| QL | Consulta propia y explicación técnica |
| Autofix y demo | Alerta, parche, pruebas y plan de contingencia |
| Semgrep y documentación | Comparación, resultados, informe y referencias |

Todos deben poder explicar por qué el SQL parametrizado corrige el problema y
por qué un parche generado requiere revisión humana.

## Evidencia visual recomendada

- Diagrama de `docs/ARQUITECTURA.md`.
- Fragmento corto del código vulnerable.
- Recorrido de datos mostrado por CodeQL.
- Diff exacto generado por Copilot Autofix.
- Resultado de la prueba de seguridad antes y después.
- Tabla comparativa basada en el mismo commit.

Evite diapositivas llenas de código. Use fragmentos de 8 a 12 líneas y deje la
ejecución completa para la demo.
