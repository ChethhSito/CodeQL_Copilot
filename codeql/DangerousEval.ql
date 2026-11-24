/**
 * @name Uso de eval en JavaScript
 * @description Detecta llamadas a eval que pueden ejecutar código arbitrario.
 * @kind problem
 * @problem.severity error
 * @security-severity 9.3
 * @precision high
 * @id grupo3/js-dangerous-eval
 * @tags security
 *       external/cwe/cwe-095
 */

import javascript

from CallExpr call
where call.getCalleeName() = "eval"
select call, "Se ejecuta texto mediante eval; utilice operaciones permitidas explícitamente."
