from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


NAVY = "18324B"
TEAL = "2C7A7B"
PALE = "EAF1F5"
PALE_ALT = "F5F8FA"
GRAY = "D9D9D9"
GREEN = "2E7D32"
RED = "B23A48"
BLACK = "000000"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=110, start=120, bottom=110, end=120) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=GRAY, size="6") -> None:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = borders.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_repeat_table_header(row) -> None:
    repeat_header(row)


def set_run_font(run, name="Aptos", size=10.5, bold=False, color=BLACK, italic=False) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def configure_document(doc: Document, short_title: str) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(BLACK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    for style_name, size, before, after in (
        ("Title", 26, 0, 14),
        ("Heading 1", 17, 10, 7),
        ("Heading 2", 13, 8, 5),
        ("Heading 3", 11, 6, 4),
    ):
        style = doc.styles[style_name]
        style.font.name = "Aptos Display" if style_name != "Heading 3" else "Aptos"
        style._element.rPr.rFonts.set(qn("w:ascii"), style.font.name)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), style.font.name)
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(BLACK)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

        # Las plantillas de Word pueden agregar un borde inferior al estilo
        # Title. Se elimina para mantener una portada académica limpia.
        if style_name == "Title":
            p_pr = style.element.get_or_add_pPr()
            p_bdr = p_pr.find(qn("w:pBdr"))
            if p_bdr is not None:
                p_pr.remove(p_bdr)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"{short_title}   |   ")
    set_run_font(run, size=8, color="666666")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    p._p.append(fld)


def add_heading(doc, text: str, level=1):
    return doc.add_heading(text, level=level)


def add_body(doc, text: str, bold_lead: str | None = None):
    p = doc.add_paragraph()
    if bold_lead and text.startswith(bold_lead):
        r = p.add_run(bold_lead)
        set_run_font(r, bold=True)
        r = p.add_run(text[len(bold_lead):])
        set_run_font(r)
    else:
        r = p.add_run(text)
        set_run_font(r)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.15)
        r = p.add_run(item)
        set_run_font(r)


def add_numbered(doc, items):
    for index, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.18)
        r = p.add_run(f"{index}. ")
        set_run_font(r, bold=True)
        r = p.add_run(item)
        set_run_font(r)


def add_code(doc, lines: list[str]) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(7)
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F2F4F5")
    p_pr.append(shd)
    for index, line in enumerate(lines):
        if index:
            p.add_run().add_break()
        r = p.add_run(line)
        set_run_font(r, name="Consolas", size=8.5, color="1F2933")


def add_table(doc, headers, rows, widths=None, font_size=8.8):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    repeat_header(table.rows[0])
    for col, header in enumerate(headers):
        cell = table.rows[0].cells[col]
        set_cell_shading(cell, NAVY)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        if widths:
            cell.width = Inches(widths[col])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(header)
        set_run_font(r, size=font_size, bold=True, color="FFFFFF")
    for row_index, row_data in enumerate(rows):
        cells = table.add_row().cells
        for col, value in enumerate(row_data):
            cell = cells[col]
            if widths:
                cell.width = Inches(widths[col])
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_index % 2:
                set_cell_shading(cell, PALE_ALT)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col == 0 or len(str(value)) > 14 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(value))
            set_run_font(r, size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_page_break(doc):
    doc.add_page_break()


def add_caption(doc, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(7)
    r = p.add_run(text)
    set_run_font(r, size=8.5, italic=True, color="555555")


def add_cover(doc, title: str, subtitle: str):
    doc.add_paragraph().paragraph_format.space_after = Pt(52)
    p = doc.add_paragraph(style="Title")
    p_pr = p._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is not None:
        p_pr.remove(p_bdr)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    set_run_font(r, name="Aptos Display", size=27, bold=True)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run(subtitle)
    set_run_font(r, size=15, color=TEAL)
    doc.add_paragraph().paragraph_format.space_after = Pt(62)
    meta = [
        ("Curso", "Seguridad Informática y Ciberseguridad"),
        ("Grupo", "Grupo 3"),
        ("Periodo", "2026 II"),
        ("Docente", "________________________________"),
        ("Integrantes", "________________________________\n________________________________\n________________________________\n________________________________\n________________________________"),
    ]
    table = doc.add_table(rows=len(meta), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    repeat_header(table.rows[0])
    for i, (label, value) in enumerate(meta):
        table.rows[i].cells[0].width = Inches(1.45)
        table.rows[i].cells[1].width = Inches(4.55)
        for cell in table.rows[i].cells:
            set_cell_margins(cell, 85, 90, 85, 90)
        p = table.rows[i].cells[0].paragraphs[0]
        r = p.add_run(label)
        set_run_font(r, size=9.5, bold=True, color=NAVY)
        p = table.rows[i].cells[1].paragraphs[0]
        r = p.add_run(value)
        set_run_font(r, size=9.5)
    add_caption(doc, "Repositorio público: github.com/ChethhSito/CodeQL_Copilot")


def build_report(output: Path, screenshot: Path | None) -> None:
    doc = Document()
    configure_document(doc, "CodeQL y Copilot Autofix")
    add_cover(doc, "Análisis estático con CodeQL y Copilot Autofix", "Detección semántica y remediación asistida en un pipeline con Semgrep")
    add_page_break(doc)

    add_heading(doc, "Resumen ejecutivo", 1)
    add_body(doc, "El proyecto implementó un laboratorio reproducible para evaluar CodeQL, Copilot Autofix y Semgrep sobre una API JavaScript con vulnerabilidades intencionales. El primer análisis produjo seis alertas: cuatro de CodeQL y dos de Semgrep. Estas alertas representaban tres problemas únicos debido a la detección superpuesta entre consultas estándar, una consulta QL propia y reglas Semgrep.")
    add_body(doc, "Copilot Autofix generó una corrección para la inyección SQL. El parche reemplazó la concatenación de entrada externa por una consulta parametrizada. La validación del pull request reveló además la ausencia de rate limiting, por lo que el grupo incorporó express-rate-limit. Las ejecuciones finales de CodeQL y Semgrep terminaron correctamente en la rama main.")
    add_table(doc, ["Indicador", "Resultado"], [
        ["Alertas iniciales", "6 alertas, 3 problemas únicos"],
        ["Corrección de Autofix", "SQL parametrizado con $1 y [category]"],
        ["Control adicional", "30 solicitudes por minuto"],
        ["Pruebas", "3 aprobadas"],
        ["Dependencias npm", "0 vulnerabilidades reportadas"],
        ["Estado final", "CodeQL y Semgrep exitosos en main"],
    ], widths=[2.3, 4.8], font_size=9)
    add_heading(doc, "Conclusión principal", 2)
    add_body(doc, "El laboratorio confirmó que CodeQL aporta contexto semántico y seguimiento de flujo, mientras Semgrep ofrece reglas rápidas y directas. Copilot Autofix redujo el tiempo necesario para preparar el parche, pero el equipo tuvo que revisar las pruebas y atender una segunda alerta antes de fusionarlo.")
    add_page_break(doc)

    add_heading(doc, "Introducción", 1)
    add_body(doc, "Los equipos de desarrollo introducen vulnerabilidades cuando incorporan entrada externa en operaciones sensibles sin una validación o separación adecuada. El análisis estático permite examinar el código antes del despliegue y convertir los hallazgos en controles dentro del proceso de integración continua.")
    add_body(doc, "Este trabajo estudia CodeQL como herramienta SAST semántica. CodeQL transforma el programa en una base de datos consultable y ejecuta reglas que modelan relaciones entre fuentes de datos, pasos de propagación y operaciones sensibles. El proyecto también evalúa Copilot Autofix como apoyo para proponer un parche revisable.")
    add_heading(doc, "Objetivo general", 2)
    add_body(doc, "Implementar y evaluar un pipeline de análisis estático con CodeQL y Copilot Autofix, integrado con Semgrep, sobre una aplicación de laboratorio controlada.")
    add_heading(doc, "Objetivos específicos", 2)
    add_bullets(doc, [
        "Configurar CodeQL y Semgrep en GitHub Actions.",
        "Crear una consulta QL para detectar llamadas a eval en JavaScript.",
        "Demostrar el recorrido de datos desde una entrada HTTP hasta una consulta SQL.",
        "Generar y revisar una corrección mediante Copilot Autofix.",
        "Comparar tiempos, hallazgos y contexto de las dos herramientas.",
    ])
    add_heading(doc, "Alcance ético", 2)
    add_body(doc, "La aplicación contiene vulnerabilidades intencionales y escucha únicamente en 127.0.0.1. El endpoint que usa eval permanece deshabilitado por defecto. El grupo ejecutó todas las pruebas en el repositorio y en ambientes autorizados.")
    add_page_break(doc)

    add_heading(doc, "Fundamentos técnicos", 1)
    add_heading(doc, "Análisis estático de aplicaciones", 2)
    add_body(doc, "SAST examina el código y sus relaciones sin depender de una sesión de ataque contra un sistema desplegado. Su utilidad dentro de CI consiste en detectar patrones de riesgo antes de fusionar un cambio. Sus resultados dependen de la cobertura de lenguajes, modelos de bibliotecas y reglas disponibles.")
    add_heading(doc, "CodeQL", 2)
    add_body(doc, "CodeQL extrae una representación relacional del programa. Las consultas QL seleccionan elementos de esa representación y pueden seguir datos entre funciones y archivos. En este proyecto, la consulta estándar js/sql-injection identificó el flujo desde req.query.category hasta pool.query.")
    add_heading(doc, "Copilot Autofix", 2)
    add_body(doc, "Copilot Autofix usa el contexto de una alerta compatible para generar una explicación y un cambio de código. El desarrollador conserva la responsabilidad de revisar el diff, ejecutar pruebas y comprobar que un nuevo análisis cierre la alerta.")
    add_heading(doc, "Semgrep", 2)
    add_body(doc, "Semgrep compara el código con patrones estructurales definidos en YAML. El grupo creó reglas para SQL concatenado y llamadas a eval. Los resultados se exportaron en formato SARIF y aparecieron junto con CodeQL en Code scanning.")
    add_table(doc, ["Concepto", "Aplicación en el proyecto"], [
        ["Fuente", "req.query.category"],
        ["Propagación", "Variable category y construcción del SQL"],
        ["Sumidero", "pool.query"],
        ["Corrección", "Parámetro $1 y arreglo [category]"],
    ], widths=[1.8, 5.3])
    add_page_break(doc)

    add_heading(doc, "Arquitectura del proyecto", 1)
    add_body(doc, "El repositorio separa la aplicación, las pruebas, las consultas QL y los workflows. GitHub Actions ejecuta ambos analizadores en cada push a main y en cada pull request dirigido a main.")
    add_table(doc, ["Componente", "Responsabilidad", "Ubicación"], [
        ["Aplicación Express", "Expone los casos de laboratorio", "src/app.js"],
        ["Pruebas", "Verifican funcionamiento y SQL parametrizado", "test/"],
        ["Consulta QL", "Detecta llamadas a eval", "codeql/DangerousEval.ql"],
        ["Configuración CodeQL", "Activa security-extended y consulta propia", ".github/codeql/"],
        ["Reglas Semgrep", "Detectan SQL concatenado y eval", "semgrep.yml"],
        ["Automatización", "Ejecuta análisis y publica SARIF", ".github/workflows/"],
    ], widths=[1.55, 3.4, 2.2], font_size=8.4)
    add_heading(doc, "Secuencia del pipeline", 2)
    add_numbered(doc, [
        "El desarrollador envía un cambio o abre un pull request.",
        "GitHub Actions instala dependencias y ejecuta las pruebas.",
        "CodeQL construye su base de datos y ejecuta consultas estándar y personalizadas.",
        "Semgrep ejecuta reglas locales y genera un archivo SARIF.",
        "GitHub presenta los hallazgos en Code scanning.",
        "Copilot Autofix prepara un parche para una alerta estándar compatible.",
    ])
    add_body(doc, "El repositorio es público y se encuentra en https://github.com/ChethhSito/CodeQL_Copilot.")
    add_page_break(doc)

    add_heading(doc, "Metodología", 1)
    add_heading(doc, "Ambiente", 2)
    add_table(doc, ["Elemento", "Configuración"], [
        ["Lenguaje", "JavaScript con Node.js 22"],
        ["Framework", "Express 5"],
        ["Base de datos", "PostgreSQL mediante pg"],
        ["CI", "GitHub Actions en ubuntu-latest"],
        ["Analizadores", "CodeQL Action v4 y Semgrep OSS"],
        ["Fecha de medición", "25 de noviembre de 2026"],
    ], widths=[2.1, 5.0])
    add_heading(doc, "Casos", 2)
    add_table(doc, ["Caso", "Debilidad", "Resultado esperado"], [
        ["A", "SQL injection CWE 89", "CodeQL y Semgrep alertan"],
        ["B", "Uso de eval CWE 95", "Consulta propia, CodeQL y Semgrep alertan"],
        ["C", "Sin rate limiting CWE 770", "CodeQL alerta"],
        ["D", "SQL parametrizado", "Las alertas SQL desaparecen"],
        ["E", "Rate limiting activo", "La alerta de saturación desaparece"],
    ], widths=[0.65, 2.65, 3.8], font_size=8.6)
    add_heading(doc, "Procedimiento", 2)
    add_numbered(doc, [
        "Publicar la versión vulnerable en main y ejecutar los workflows.",
        "Registrar las alertas y el recorrido de datos.",
        "Generar un parche con Copilot Autofix para la alerta SQL.",
        "Ejecutar pruebas en el pull request y corregir controles adicionales.",
        "Fusionar el pull request y repetir los análisis sobre main.",
    ])
    add_page_break(doc)

    add_heading(doc, "Detección inicial", 1)
    add_body(doc, "La primera ejecución produjo seis alertas. CodeQL reportó SQL injection, code injection, falta de rate limiting y la alerta de la consulta personalizada. Semgrep reportó SQL concatenado y eval.")
    if screenshot and screenshot.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        picture = p.add_run().add_picture(str(screenshot), width=Inches(5.25))
        picture._inline.docPr.set("descr", "Lista de seis alertas iniciales de CodeQL y Semgrep en GitHub Code scanning")
        picture._inline.docPr.set("title", "Alertas iniciales en Code scanning")
        add_caption(doc, "Figura 1. Alertas iniciales en GitHub Code scanning")
    add_table(doc, ["Problema único", "Detectores", "Estado inicial"], [
        ["Uso de eval", "CodeQL personalizado, CodeQL estándar y Semgrep", "3 alertas"],
        ["SQL injection", "CodeQL estándar y Semgrep", "2 alertas"],
        ["Falta de rate limiting", "CodeQL estándar", "1 alerta"],
    ], widths=[1.7, 3.8, 1.6], font_size=8.4)
    add_page_break(doc)

    add_heading(doc, "Consulta QL personalizada", 1)
    add_body(doc, "El grupo creó una consulta de tipo problem para localizar llamadas a eval. El objetivo fue demostrar la estructura básica de QL con un caso verificable y separado de Autofix.")
    add_code(doc, [
        "/**",
        " * @name Uso de eval en JavaScript",
        " * @kind problem",
        " * @id grupo3/js-dangerous-eval",
        " * @tags security external/cwe/cwe-095",
        " */",
        "import javascript",
        "from CallExpr call",
        "where call.getCalleeName() = \"eval\"",
        "select call, \"Se ejecuta texto mediante eval\"",
    ])
    add_heading(doc, "Lectura de la consulta", 2)
    add_table(doc, ["Parte", "Función"], [
        ["Metadatos", "Identifican la regla, severidad, precisión y CWE"],
        ["import", "Carga el modelo de JavaScript"],
        ["from", "Declara la expresión de llamada que se analizará"],
        ["where", "Filtra llamadas cuyo nombre de función es eval"],
        ["select", "Define la ubicación y el mensaje de la alerta"],
    ], widths=[1.45, 5.65])
    add_body(doc, "La consulta personalizada sí generó una alerta en Code scanning. El equipo no la usó para demostrar Autofix porque las correcciones automáticas se deben evaluar con una alerta estándar compatible.")
    add_page_break(doc)

    add_heading(doc, "Integración con GitHub Actions", 1)
    add_heading(doc, "Workflow de CodeQL", 2)
    add_body(doc, "El workflow inicializa CodeQL para javascript-typescript, usa la configuración local, instala Node.js, ejecuta pruebas y publica el análisis. La configuración agrega security-extended y el paquete local codeql.")
    add_code(doc, [
        "- uses: github/codeql-action/init@v4",
        "  with:",
        "    languages: javascript-typescript",
        "    config-file: ./.github/codeql/codeql-config.yml",
        "- run: npm ci && npm test && npm run test:security",
        "- uses: github/codeql-action/analyze@v4",
    ])
    add_heading(doc, "Workflow de Semgrep", 2)
    add_body(doc, "Semgrep instala su CLI, ejecuta semgrep.yml, genera SARIF y publica el resultado mediante github/codeql-action/upload-sarif@v4. Este diseño permite revisar los resultados de ambas herramientas en la misma interfaz.")
    add_code(doc, [
        "semgrep scan --config semgrep.yml --sarif --output semgrep.sarif src",
        "github/codeql-action/upload-sarif@v4",
    ])
    add_heading(doc, "Control de integración", 2)
    add_body(doc, "Las pruebas de seguridad forman parte del workflow de CodeQL. Una futura regresión que vuelva a concatenar la categoría en el SQL hará fallar el pipeline antes de la fusión.")
    add_page_break(doc)

    add_heading(doc, "Corrección con Copilot Autofix", 1)
    add_body(doc, "El equipo abrió la alerta Database query built from user-controlled sources y solicitó una corrección. Autofix creó la rama alert-autofix-5 y un pull request en borrador.")
    add_heading(doc, "Código anterior", 2)
    add_code(doc, [
        "const sql = \"SELECT ... WHERE category = '\" + category + \"' ORDER BY name\";",
        "const result = await pool.query(sql);",
    ])
    add_heading(doc, "Código propuesto", 2)
    add_code(doc, [
        "const sql = \"SELECT ... WHERE category = $1 ORDER BY name\";",
        "const result = await pool.query(sql, [category]);",
    ])
    add_body(doc, "La consulta parametrizada separa la instrucción SQL del valor controlado por el usuario. PostgreSQL interpreta category como un dato asociado al marcador $1 y no como parte de la sintaxis.")
    add_heading(doc, "Revisión del parche", 2)
    add_bullets(doc, [
        "El diff modificó solamente la construcción y ejecución de la consulta.",
        "La prueba de seguridad verificó dos argumentos en pool.query.",
        "Semgrep dejó de reportar SQL concatenado.",
        "CodeQL dejó de reportar el flujo hacia una consulta construida con entrada externa.",
    ])
    add_page_break(doc)

    add_heading(doc, "Validación y segundo control", 1)
    add_body(doc, "La primera ejecución del pull request falló porque una prueba antigua esperaba que el texto de ataque apareciera dentro del SQL. El grupo actualizó esa prueba para comprobar el comportamiento seguro y agregó npm run test:security al workflow.")
    add_body(doc, "Después de corregir las pruebas, CodeQL identificó Missing rate limiting en el endpoint que accedía a la base de datos. El equipo incorporó express-rate-limit antes de fusionar el pull request.")
    add_code(doc, [
        "const limiter = RateLimit({",
        "  windowMs: 60 * 1000,",
        "  max: 30,",
        "  standardHeaders: true,",
        "  legacyHeaders: false,",
        "});",
        "app.use(limiter);",
    ])
    add_table(doc, ["Validación", "Resultado"], [
        ["npm test", "2 pruebas funcionales aprobadas"],
        ["npm run test:security", "1 prueba de seguridad aprobada"],
        ["npm audit", "0 vulnerabilidades reportadas"],
        ["Semgrep local", "Solo permaneció la regla intencional de eval"],
        ["Checks del PR", "4 resultados aprobados"],
        ["Fusión", "PR 1 fusionado en main"],
    ], widths=[2.4, 4.7])
    add_page_break(doc)

    add_heading(doc, "Resultados", 1)
    add_heading(doc, "Duración de los workflows", 2)
    add_table(doc, ["Etapa", "CodeQL", "Semgrep"], [
        ["Análisis inicial en main", "96 s", "38 s"],
        ["Análisis final en main", "93 s", "25 s"],
        ["Cambio", "3 s menos", "13 s menos"],
    ], widths=[3.1, 1.9, 1.9], font_size=9)
    add_body(doc, "Los tiempos corresponden a los jobs de GitHub Actions del 25 de noviembre de 2026. Son observaciones de este repositorio y no representan un benchmark general.")
    add_heading(doc, "Estado de los hallazgos", 2)
    add_table(doc, ["Hallazgo", "Antes", "Después"], [
        ["SQL injection CodeQL", "Abierto", "Corregido"],
        ["SQL concatenado Semgrep", "Abierto", "Corregido"],
        ["Missing rate limiting", "Abierto", "Corregido"],
        ["Eval consulta personalizada", "Abierto", "Abierto por diseño"],
        ["Code injection", "Abierto", "Abierto por diseño"],
        ["Eval Semgrep", "Abierto", "Abierto por diseño"],
    ], widths=[3.6, 1.5, 1.8], font_size=8.7)
    add_heading(doc, "Ejecuciones reproducibles", 2)
    add_table(doc, ["Workflow", "Run ID", "Commit", "Resultado"], [
        ["CodeQL inicial", "45657346922", "83cdc22", "Éxito"],
        ["Semgrep inicial", "45657347138", "83cdc22", "Éxito"],
        ["CodeQL final", "45674463710", "8dd28ee", "Éxito"],
        ["Semgrep final", "45674463631", "8dd28ee", "Éxito"],
    ], widths=[2.0, 1.65, 1.4, 1.5], font_size=8.5)
    add_page_break(doc)

    add_heading(doc, "Comparación entre CodeQL y Semgrep", 1)
    add_table(doc, ["Criterio", "CodeQL", "Semgrep"], [
        ["Modelo", "Base de datos semántica y consultas QL", "Patrones estructurales YAML"],
        ["Flujo de datos", "Muestra fuente, propagación y sumidero", "La regla local fue sintáctica"],
        ["Tiempo inicial", "96 segundos", "38 segundos"],
        ["Consulta propia", "DangerousEval.ql", "Dos reglas en semgrep.yml"],
        ["Corrección asistida", "Copilot Autofix en alerta compatible", "No se usó Autofix"],
        ["Hallazgo adicional", "Missing rate limiting", "No detectado por reglas locales"],
    ], widths=[1.55, 2.85, 2.85], font_size=8.2)
    add_heading(doc, "Interpretación", 2)
    add_body(doc, "Semgrep terminó más rápido en las dos mediciones y detectó los patrones definidos por el grupo. CodeQL tardó más, pero aportó el recorrido de datos y detectó la ausencia de rate limiting sin que el grupo escribiera una regla adicional. Los resultados apoyan un pipeline combinado: Semgrep ofrece retroalimentación rápida y CodeQL agrega profundidad semántica.")
    add_heading(doc, "Limitaciones", 2)
    add_bullets(doc, [
        "El laboratorio contiene pocos archivos y dos vulnerabilidades intencionales.",
        "Los tiempos dependen de GitHub Actions, la red y las versiones de las herramientas.",
        "Las seis alertas iniciales no equivalen a seis vulnerabilidades únicas.",
        "Autofix trabaja sobre un subconjunto de alertas y siempre requiere revisión.",
        "El caso eval permanece abierto para demostrar la consulta personalizada.",
    ])
    add_page_break(doc)

    add_heading(doc, "Conclusiones", 1)
    add_body(doc, "El proyecto cumplió el objetivo de implementar CodeQL, una consulta QL propia, Copilot Autofix y Semgrep dentro de un pipeline reproducible. El primer análisis identificó tres problemas únicos mediante seis alertas superpuestas.")
    add_body(doc, "Copilot Autofix preparó una corrección válida para SQL injection. La revisión del pull request permitió detectar una prueba incompatible con el nuevo comportamiento y una segunda debilidad relacionada con rate limiting. El grupo corrigió ambos puntos antes de fusionar el cambio.")
    add_body(doc, "La comparación mostró que Semgrep completó el análisis inicial en 38 segundos y CodeQL en 96 segundos. CodeQL aportó contexto adicional y una alerta que no estaba cubierta por las reglas locales. El pipeline combinado conserva ambas ventajas.")
    add_heading(doc, "Recomendaciones", 2)
    add_bullets(doc, [
        "Mantener las pruebas funcionales y de seguridad como requisito de los pull requests.",
        "Revisar cada parche generado antes de fusionarlo.",
        "Actualizar consultas y versiones de Actions de forma controlada.",
        "Eliminar eval en una rama posterior y sustituirlo por operaciones permitidas.",
    ])
    add_heading(doc, "Referencias", 1)
    refs = [
        "[1] GitHub, CodeQL code scanning. https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning",
        "[2] GitHub, Autofix for code scanning. https://docs.github.com/en/code-security/concepts/code-scanning/autofix-for-code-scanning",
        "[3] GitHub, Custom CodeQL queries. https://docs.github.com/en/code-security/concepts/code-scanning/codeql/custom-queries",
        "[4] CodeQL, Database query built from user-controlled sources. https://codeql.github.com/codeql-query-help/javascript/js-sql-injection/",
        "[5] CodeQL, Missing rate limiting. https://codeql.github.com/codeql-query-help/javascript/js-missing-rate-limiting/",
        "[6] Semgrep, Sample CI configurations. https://semgrep.dev/docs/semgrep-ci/sample-ci-configs",
        "[7] MITRE, CWE-89 SQL Injection. https://cwe.mitre.org/data/definitions/89.html",
        "[8] MITRE, CWE-95 Eval Injection. https://cwe.mitre.org/data/definitions/95.html",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(ref)
        set_run_font(r, size=8.4)

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def build_guide(output: Path) -> None:
    doc = Document()
    configure_document(doc, "Guion de demo y video")
    add_cover(doc, "Guion de demostración y video de respaldo", "CodeQL y Copilot Autofix con integración de Semgrep")
    add_page_break(doc)

    add_heading(doc, "Preparación de la demostración", 1)
    add_heading(doc, "Archivos y pestañas", 2)
    add_bullets(doc, [
        "Repositorio abierto en la pestaña principal.",
        "Security and quality con filtros is:closed branch:main e is:open branch:main.",
        "Pull request 1 abierto en Files changed y Checks.",
        "Ejecuciones finales de CodeQL y Semgrep abiertas.",
        "Editor ubicado en src/app.js, DangerousEval.ql y semgrep.yml.",
    ])
    add_heading(doc, "Evidencias", 2)
    add_bullets(doc, [
        "Captura de las seis alertas iniciales.",
        "Captura del recorrido de datos de SQL injection.",
        "Diff original de Copilot Autofix.",
        "Checks finales aprobados.",
        "Alertas corregidas y alertas de eval que permanecen abiertas.",
    ])
    add_heading(doc, "Comprobaciones previas", 2)
    add_numbered(doc, [
        "Ejecutar npm test y npm run test:security.",
        "Confirmar que main apunta al commit 8dd28ee.",
        "Probar audio, resolución y tamaño del texto.",
        "Cerrar notificaciones y ocultar información personal.",
        "Tener el video de respaldo disponible sin conexión.",
    ])
    add_page_break(doc)

    add_heading(doc, "Guion de demo de 15 minutos", 1)
    add_table(doc, ["Tiempo", "Acción", "Explicación"], [
        ["0:00 a 1:30", "Presentar objetivo", "Detección, corrección y validación en CI"],
        ["1:30 a 3:30", "Mostrar código vulnerable", "Entrada HTTP, SQL concatenado y eval"],
        ["3:30 a 6:00", "Abrir alertas iniciales", "Seis alertas y tres problemas únicos"],
        ["6:00 a 8:00", "Explicar QL propia", "Metadatos, from, where y select"],
        ["8:00 a 10:30", "Mostrar Autofix", "Diff con $1 y [category]"],
        ["10:30 a 12:30", "Mostrar validación", "Pruebas y rate limiting"],
        ["12:30 a 14:00", "Comparar herramientas", "Tiempos y diferencias"],
        ["14:00 a 15:00", "Cerrar con resultados", "Checks verdes y alertas corregidas"],
    ], widths=[1.05, 2.25, 3.8], font_size=8.2)
    add_heading(doc, "Frases clave", 2)
    add_bullets(doc, [
        "Las seis alertas representan tres problemas únicos porque varias reglas detectan el mismo código.",
        "La consulta parametrizada separa el comando SQL del valor recibido.",
        "Autofix propuso el cambio, pero las pruebas y CodeQL determinaron si era aceptable.",
        "Semgrep fue más rápido en este laboratorio y CodeQL aportó mayor contexto.",
    ])
    add_page_break(doc)

    add_heading(doc, "Reparto de exposición de 30 a 35 minutos", 1)
    add_table(doc, ["Rol", "Minutos", "Contenido"], [
        ["Integrante 1", "0 a 6", "Problema, objetivos y alcance ético"],
        ["Integrante 2", "6 a 13", "Arquitectura de CodeQL y flujo de datos"],
        ["Integrante 3", "13 a 19", "Consulta QL propia y configuración"],
        ["Integrante 4", "19 a 27", "Autofix, pull request y pruebas"],
        ["Integrante 5", "27 a 34", "Semgrep, resultados, límites y cierre"],
    ], widths=[1.6, 1.2, 4.35], font_size=8.8)
    add_heading(doc, "Preguntas probables", 2)
    add_table(doc, ["Pregunta", "Respuesta breve"], [
        ["¿Por qué hay alertas duplicadas?", "Consultas distintas pueden señalar el mismo problema desde modelos diferentes."],
        ["¿Autofix garantiza seguridad?", "No. El equipo revisa el diff, ejecuta pruebas y repite el análisis."],
        ["¿Por qué usar dos herramientas?", "Semgrep aporta velocidad y CodeQL agrega análisis semántico."],
        ["¿Por qué eval sigue abierto?", "Se conserva como caso de la consulta QL y está deshabilitado por defecto."],
        ["¿Qué corrigió el rate limiter?", "Reduce solicitudes repetidas que podrían saturar el acceso a la base de datos."],
    ], widths=[2.7, 4.45], font_size=8.5)
    add_page_break(doc)

    add_heading(doc, "Plan del video de respaldo", 1)
    add_heading(doc, "Duración y formato", 2)
    add_body(doc, "Grabar un video de 12 a 15 minutos en 1080p. Mostrar la pantalla completa, usar un tamaño de fuente legible y grabar la narración en español. Evitar datos personales, pestañas de mensajería y notificaciones.")
    add_heading(doc, "Secuencia de grabación", 2)
    add_numbered(doc, [
        "Presentar el repositorio y el propósito del laboratorio.",
        "Mostrar el código vulnerable mediante el historial o la captura inicial.",
        "Abrir las alertas iniciales y explicar los duplicados.",
        "Mostrar la consulta DangerousEval.ql.",
        "Abrir el pull request y explicar el parche de Autofix.",
        "Mostrar la prueba de seguridad y el rate limiter.",
        "Abrir las ejecuciones finales y cerrar con la tabla de resultados.",
    ])
    add_heading(doc, "Respaldo técnico", 2)
    add_bullets(doc, [
        "Guardar el archivo en MP4 con codificación H.264.",
        "Conservar una copia local y otra en el medio de entrega autorizado.",
        "Reproducir el archivo completo antes de entregarlo.",
        "Anotar el commit 8dd28ee y los Run IDs finales en la descripción.",
    ])
    add_page_break(doc)

    add_heading(doc, "Lista final de entrega", 1)
    add_table(doc, ["Elemento", "Estado", "Observación"], [
        ["Informe PDF máximo 15 páginas", "Listo para completar", "Añadir nombres y docente"],
        ["Presentación", "Lista para revisar", "Asignar expositor por diapositiva"],
        ["Repositorio público", "Completo", "main en commit 8dd28ee"],
        ["Video de respaldo", "Pendiente de grabación", "Usar este guion"],
        ["Evidencias", "Pendiente de organizar", "Guardar capturas en orden"],
    ], widths=[2.35, 1.65, 3.15], font_size=8.8)
    add_heading(doc, "Enlaces", 2)
    add_body(doc, "Repositorio: https://github.com/ChethhSito/CodeQL_Copilot")
    add_body(doc, "Pull request: https://github.com/ChethhSito/CodeQL_Copilot/pull/1")
    add_body(doc, "CodeQL final: https://github.com/ChethhSito/CodeQL_Copilot/actions/runs/45674463710")
    add_body(doc, "Semgrep final: https://github.com/ChethhSito/CodeQL_Copilot/actions/runs/45674463631")
    add_heading(doc, "Antes de presentar", 2)
    add_body(doc, "Completar nombres, código de estudiante, docente y fecha. Ensayar con cronómetro y reemplazar cualquier captura que muestre información personal.")

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--screenshot")
    args = parser.parse_args()
    out = Path(args.output_dir)
    screenshot = Path(args.screenshot) if args.screenshot else None
    build_report(out / "Informe_Tecnico_CodeQL_Copilot_Autofix.docx", screenshot)
    build_guide(out / "Guion_Demo_Video_Backup.docx")


if __name__ == "__main__":
    main()
