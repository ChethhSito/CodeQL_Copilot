# CodeQL y Copilot Autofix para análisis y remediación de vulnerabilidades

## Resumen

Este proyecto evalúa un flujo de análisis estático sobre una API JavaScript de
laboratorio. CodeQL detecta vulnerabilidades mediante análisis semántico y flujo
de datos; Copilot Autofix propone cambios para alertas estándar compatibles; y
Semgrep aporta una revisión rápida basada en reglas. La evaluación considera la
capacidad de detección, la explicación del hallazgo, el tiempo de ejecución y la
validación posterior de la corrección.

## 1. Introducción

Describa el problema de incorporar código vulnerable durante el desarrollo, el
objetivo general y el alcance académico. Indique que el sistema se ejecuta solo
en un ambiente autorizado.

## 2. Fundamentos

### 2.1 Análisis estático de aplicaciones

Defina SAST, ventajas y límites. Diferencie coincidencia sintáctica de análisis
semántico sin presentar una como reemplazo total de la otra.

### 2.2 CodeQL

Explique extracción, base de datos relacional, librerías del lenguaje, consultas
QL y presentación de resultados SARIF.

### 2.3 Copilot Autofix

Explique que produce una sugerencia revisable para alertas compatibles. Destaque
que el equipo debe revisar y probar la modificación antes de integrarla.

### 2.4 Semgrep

Resuma su modelo de reglas y el papel que cumple en el pipeline combinado.

## 3. Metodología

### 3.1 Ambiente

Registre sistema operativo, versiones, visibilidad del repositorio, commit
analizado y fecha de la medición.

### 3.2 Casos de prueba

- Caso A: entrada HTTP concatenada dentro de SQL, CWE-89.
- Caso B: ejecución de texto con `eval`, CWE-95.
- Caso C: versión corregida con consulta parametrizada.

### 3.3 Procedimiento reproducible

Documente instalación, pruebas, ejecución de workflows, revisión de alertas,
generación de la sugerencia, aplicación del parche y segundo análisis.

## 4. Implementación

Incluya la arquitectura, fragmentos mínimos del código, configuración de CodeQL,
consulta QL propia y reglas Semgrep. Explique cada decisión sin copiar archivos
completos.

## 5. Resultados

Complete la tabla con mediciones reales del mismo commit y runner.

| Métrica | CodeQL | Semgrep |
|---|---:|---:|
| Duración del workflow | Pendiente | Pendiente |
| Alertas verdaderas del laboratorio | Pendiente | Pendiente |
| Alertas no esperadas | Pendiente | Pendiente |
| Muestra recorrido de datos | Sí/No | Sí/No |
| Corrección automática observada | Sí/No | No aplica |

No afirme porcentajes de precisión con solo dos casos. Presente los resultados
como observaciones del laboratorio y explique el tamaño limitado de la muestra.

## 6. Evaluación del parche

Compare el código anterior y posterior. Registre si la sugerencia usó parámetros,
si conservó el comportamiento y si `npm run test:security` pasó. Mencione ajustes
manuales, si los hubo.

## 7. Comparación e integración

Analice velocidad, profundidad, facilidad de reglas y calidad del contexto.
Explique por qué el pipeline usa ambos resultados en Code scanning.

## 8. Limitaciones

Incluya dependencia de GitHub, compatibilidad parcial de Autofix, tamaño del
laboratorio, posibles falsos positivos y diferencia respecto de producción.

## 9. Conclusiones

Responda si se cumplieron los objetivos usando las evidencias de la sección de
resultados. Evite generalizar más allá del experimento.

## Referencias sugeridas

- Documentación oficial de CodeQL y GitHub Code Security.
- Ayuda oficial de la consulta `js/sql-injection`.
- Documentación oficial de Semgrep.
- OWASP y MITRE CWE-89/CWE-95.

Use el formato de referencias pedido por el docente y registre fecha de consulta.
