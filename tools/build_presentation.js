const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Grupo 3';
pptx.subject = 'CodeQL, Copilot Autofix y Semgrep';
pptx.title = 'CodeQL y Copilot Autofix — Grupo 3';
pptx.company = 'Proyecto académico';
pptx.lang = 'es-PE';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'es-PE'
};

const C = {
  navy: '18324B',
  navy2: '0F2437',
  teal: '2C7A7B',
  green: '2E7D32',
  red: 'B23A48',
  amber: 'B7791F',
  ink: '111827',
  muted: '52606D',
  light: 'F5F8FA',
  pale: 'E8F1F5',
  white: 'FFFFFF',
  line: 'CED7DE'
};

const W = 13.333;
const H = 7.5;

function baseSlide(title, section) {
  const s = pptx.addSlide();
  s.background = { color: C.light };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: 0.16, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText(title, { x: 0.72, y: 0.38, w: 11.85, h: 0.48, fontFace: 'Aptos Display', fontSize: 26, bold: true, color: C.ink, margin: 0 });
  if (section) s.addText(section.toUpperCase(), { x: 0.75, y: 0.93, w: 3.4, h: 0.22, fontSize: 9.5, bold: true, color: C.teal, charSpacing: 1.2, margin: 0 });
  s.addShape(pptx.ShapeType.line, { x: 0.72, y: 7.08, w: 11.9, h: 0, line: { color: C.line, width: 1 } });
  s.addText('Grupo 3  ·  CodeQL + Copilot Autofix', { x: 0.75, y: 7.15, w: 5, h: 0.16, fontSize: 8.5, color: C.muted, margin: 0 });
  s.addText(String(pptx._slides.length), { x: 12.08, y: 7.15, w: 0.45, h: 0.16, fontSize: 8.5, color: C.muted, align: 'right', margin: 0 });
  return s;
}

function addBulletList(slide, items, x, y, w, h, fontSize = 18, color = C.ink) {
  const runs = [];
  items.forEach((item, i) => {
    runs.push({ text: item, options: { bullet: { indent: 18 }, breakLine: i < items.length - 1 } });
  });
  slide.addText(runs, { x, y, w, h, fontSize, color, breakLine: false, margin: 0.04, paraSpaceAfterPt: 10, valign: 'top', fit: 'shrink' });
}

function addLabel(slide, text, x, y, w, color = C.teal) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.34, rectRadius: 0.05, fill: { color }, line: { color } });
  slide.addText(text, { x, y: y + 0.055, w, h: 0.16, align: 'center', fontSize: 10, bold: true, color: C.white, margin: 0 });
}

function addCode(slide, title, lines, x, y, w, h, accent = C.teal) {
  slide.addText(title, { x, y: y - 0.32, w, h: 0.22, fontSize: 13, bold: true, color: accent, margin: 0 });
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.04, fill: { color: 'EEF2F4' }, line: { color: C.line, width: 1 } });
  slide.addText(lines.join('\n'), { x: x + 0.16, y: y + 0.14, w: w - 0.3, h: h - 0.25, fontFace: 'Consolas', fontSize: 11.5, color: C.navy2, margin: 0, breakLine: false, fit: 'shrink', valign: 'mid' });
}

function addMetric(slide, value, label, x, y, color) {
  slide.addText(value, { x, y, w: 1.65, h: 0.72, fontSize: 34, bold: true, color, align: 'center', margin: 0 });
  slide.addText(label, { x, y: y + 0.75, w: 1.65, h: 0.48, fontSize: 12.5, color: C.muted, align: 'center', margin: 0.02, fit: 'shrink' });
}

// 1 — Portada
{
  const s = pptx.addSlide();
  s.background = { color: C.navy2 };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.22, h: H, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText('CODEQL  +  COPILOT AUTOFIX', { x: 0.85, y: 0.82, w: 7.7, h: 0.28, fontSize: 12, bold: true, color: '7DD3D1', charSpacing: 2.2, margin: 0 });
  s.addText('Análisis estático y\nremediación asistida', { x: 0.82, y: 1.35, w: 8.6, h: 1.75, fontFace: 'Aptos Display', fontSize: 36, bold: true, color: C.white, margin: 0, breakLine: false });
  s.addText('Pipeline reproducible con CodeQL, una consulta QL propia y Semgrep', { x: 0.86, y: 3.45, w: 7.35, h: 0.62, fontSize: 19, color: 'D7E4EA', margin: 0 });
  s.addShape(pptx.ShapeType.line, { x: 0.86, y: 4.45, w: 4.8, h: 0, line: { color: C.teal, width: 3 } });
  s.addText('GRUPO 3', { x: 0.86, y: 4.72, w: 2.1, h: 0.34, fontSize: 17, bold: true, color: C.white, margin: 0 });
  s.addText('Seguridad Informática y Ciberseguridad · 2026 II', { x: 0.86, y: 5.18, w: 5.9, h: 0.28, fontSize: 13.5, color: 'B9CAD3', margin: 0 });
  s.addText('Integrantes: completar nombres', { x: 0.86, y: 5.65, w: 5.2, h: 0.26, fontSize: 12, italic: true, color: '8FA6B2', margin: 0 });
  s.addShape(pptx.ShapeType.arc, { x: 9.1, y: 1.18, w: 2.6, h: 2.6, adjustPoint: 0.25, rotate: 18, fill: { color: C.teal, transparency: 78 }, line: { color: '7DD3D1', transparency: 35, width: 2.5 } });
  s.addShape(pptx.ShapeType.arc, { x: 9.75, y: 1.83, w: 2.6, h: 2.6, adjustPoint: 0.25, rotate: 198, fill: { color: C.navy, transparency: 100 }, line: { color: C.white, transparency: 55, width: 2.5 } });
  s.addText('{ QL }', { x: 9.62, y: 2.32, w: 2.0, h: 0.72, fontFace: 'Consolas', fontSize: 26, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('Repositorio: github.com/ChethhSito/CodeQL_Copilot', { x: 0.86, y: 6.85, w: 6.4, h: 0.18, fontSize: 8.5, color: '8FA6B2', margin: 0 });
}

// 2 — Problema y objetivos
{
  const s = baseSlide('Problema y objetivos', 'Contexto');
  s.addText('¿Cómo detectar, corregir y verificar vulnerabilidades antes de fusionar código?', { x: 0.78, y: 1.38, w: 11.7, h: 0.62, fontSize: 24, bold: true, color: C.navy, margin: 0, fit: 'shrink' });
  addBulletList(s, [
    'Configurar CodeQL y Semgrep en GitHub Actions.',
    'Crear una consulta QL para localizar llamadas a eval.',
    'Generar y revisar una corrección con Copilot Autofix.',
    'Validar el cambio con pruebas y un nuevo análisis.',
    'Comparar cobertura, contexto y tiempo de ambas herramientas.'
  ], 0.95, 2.35, 7.0, 3.45, 18.5);
  s.addShape(pptx.ShapeType.roundRect, { x: 8.55, y: 2.1, w: 3.75, h: 3.3, rectRadius: 0.05, fill: { color: C.pale }, line: { color: C.teal, width: 1.5 } });
  s.addText('ALCANCE ÉTICO', { x: 8.9, y: 2.48, w: 3.05, h: 0.28, fontSize: 14, bold: true, color: C.teal, align: 'center', margin: 0 });
  s.addText('Laboratorio controlado\n\nServidor local en 127.0.0.1\n\nVulnerabilidades intencionales\n\nSin pruebas contra terceros', { x: 8.95, y: 2.98, w: 2.95, h: 1.9, fontSize: 16, color: C.ink, align: 'center', margin: 0.02, breakLine: false, fit: 'shrink' });
}

// 3 — Flujo SAST
{
  const s = baseSlide('El pipeline SAST del proyecto', 'Proceso');
  const xs = [0.7, 3.15, 5.6, 8.05, 10.5];
  const titles = ['Código', 'GitHub Actions', 'CodeQL + Semgrep', 'Code scanning', 'Revisión'];
  const desc = ['push / PR', 'pruebas y build', 'análisis estático', 'alertas SARIF', 'Autofix + equipo'];
  xs.forEach((x, i) => {
    s.addShape(pptx.ShapeType.roundRect, { x, y: 2.3, w: 2.05, h: 1.55, rectRadius: 0.05, fill: { color: i === 2 ? C.navy : C.white }, line: { color: i === 2 ? C.navy : C.line, width: 1.5 } });
    s.addText(titles[i], { x: x + 0.12, y: 2.65, w: 1.81, h: 0.28, fontSize: 15, bold: true, color: i === 2 ? C.white : C.navy, align: 'center', margin: 0, fit: 'shrink' });
    s.addText(desc[i], { x: x + 0.12, y: 3.08, w: 1.81, h: 0.34, fontSize: 11.5, color: i === 2 ? 'D7E4EA' : C.muted, align: 'center', margin: 0, fit: 'shrink' });
    if (i < xs.length - 1) s.addShape(pptx.ShapeType.chevron, { x: x + 2.08, y: 2.82, w: 0.34, h: 0.48, fill: { color: C.teal }, line: { color: C.teal } });
  });
  s.addText('Cada pull request repite el ciclo y evita que una corrección se acepte sin pruebas.', { x: 1.25, y: 4.65, w: 10.8, h: 0.5, fontSize: 21, color: C.ink, align: 'center', margin: 0 });
  addLabel(s, 'detección', 3.05, 5.65, 1.65, C.red);
  addLabel(s, 'corrección', 5.3, 5.65, 1.65, C.teal);
  addLabel(s, 'verificación', 7.55, 5.65, 1.65, C.green);
}

// 4 — Arquitectura CodeQL
{
  const s = baseSlide('Cómo trabaja CodeQL', 'Fundamentos');
  const items = [
    ['1', 'Código fuente', 'JavaScript y dependencias'],
    ['2', 'Base de datos', 'Representación relacional'],
    ['3', 'Consultas QL', 'Reglas estándar + propias'],
    ['4', 'Resultado', 'Ruta de datos y alerta']
  ];
  items.forEach((it, i) => {
    const x = 0.8 + i * 3.12;
    s.addShape(pptx.ShapeType.ellipse, { x, y: 2.0, w: 0.64, h: 0.64, fill: { color: i === 3 ? C.green : C.teal }, line: { color: i === 3 ? C.green : C.teal } });
    s.addText(it[0], { x, y: 2.12, w: 0.64, h: 0.24, fontSize: 16, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(it[1], { x: x - 0.42, y: 2.9, w: 1.5, h: 0.36, fontSize: 17, bold: true, color: C.navy, align: 'center', margin: 0, fit: 'shrink' });
    s.addText(it[2], { x: x - 0.63, y: 3.4, w: 1.92, h: 0.62, fontSize: 13, color: C.muted, align: 'center', margin: 0.02, fit: 'shrink' });
    if (i < items.length - 1) s.addShape(pptx.ShapeType.line, { x: x + 0.72, y: 2.32, w: 2.24, h: 0, line: { color: C.line, width: 2, beginArrowType: 'none', endArrowType: 'triangle' } });
  });
  s.addText('Ventaja clave', { x: 0.93, y: 5.1, w: 2, h: 0.3, fontSize: 14, bold: true, color: C.teal, margin: 0 });
  s.addText('No busca únicamente texto: puede seguir una entrada externa desde su fuente, a través de variables, hasta una operación sensible.', { x: 0.93, y: 5.48, w: 11.2, h: 0.75, fontSize: 19, color: C.ink, margin: 0, fit: 'shrink' });
}

// 5 — Estructura del laboratorio
{
  const s = baseSlide('Estructura del laboratorio', 'Implementación');
  s.addTable([
    [{ text: 'Componente', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }, { text: 'Función', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }, { text: 'Ubicación', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }],
    ['Aplicación Express', 'Casos vulnerables controlados', 'src/app.js'],
    ['Pruebas', 'Funcionalidad y SQL parametrizado', 'test/'],
    ['Consulta QL', 'Detecta llamadas a eval', 'codeql/DangerousEval.ql'],
    ['Reglas Semgrep', 'SQL concatenado y eval', 'semgrep.yml'],
    ['Workflows', 'Analizan y publican SARIF', '.github/workflows/']
  ], {
    x: 0.82, y: 1.55, w: 11.7, h: 3.85,
    border: { type: 'solid', pt: 1, color: C.line },
    fill: C.white, color: C.ink, fontSize: 13.5,
    rowH: 0.62, margin: 0.09,
    colW: [2.25, 5.45, 4.0],
    autoFit: false,
    bold: false
  });
  s.addText('Repositorio público y reproducible', { x: 0.98, y: 5.85, w: 3.2, h: 0.34, fontSize: 15, bold: true, color: C.teal, margin: 0 });
  s.addText('github.com/ChethhSito/CodeQL_Copilot', { x: 4.1, y: 5.85, w: 5.0, h: 0.34, fontSize: 15, color: C.navy, margin: 0 });
}

// 6 — Vulnerabilidad SQL
{
  const s = baseSlide('Caso principal: SQL injection', 'Detección');
  addCode(s, 'Código vulnerable', [
    'const category = req.query.category;',
    'const sql = "SELECT ... WHERE category = \'"',
    '  + category + "\' ORDER BY name";',
    'await pool.query(sql);'
  ], 0.78, 1.75, 5.55, 2.45, C.red);
  s.addShape(pptx.ShapeType.line, { x: 6.62, y: 2.95, w: 0.85, h: 0, line: { color: C.red, width: 2.5, endArrowType: 'triangle' } });
  s.addShape(pptx.ShapeType.roundRect, { x: 7.72, y: 1.72, w: 4.72, h: 2.55, rectRadius: 0.04, fill: { color: 'FCEEEF' }, line: { color: C.red, width: 1.5 } });
  s.addText('Recorrido detectado', { x: 8.05, y: 2.05, w: 4.05, h: 0.3, fontSize: 17, bold: true, color: C.red, align: 'center', margin: 0 });
  s.addText('Fuente\nreq.query.category\n\nPropagación\nvariable + concatenación\n\nSumidero\npool.query(sql)', { x: 8.05, y: 2.78, w: 4.05, h: 1.16, fontSize: 13.2, color: C.ink, align: 'center', margin: 0, breakLine: false, fit: 'shrink' });
  s.addText('La entrada del usuario pasa a formar parte de la sintaxis SQL. Por eso CodeQL y Semgrep señalan el mismo problema desde modelos diferentes.', { x: 0.95, y: 5.05, w: 11.35, h: 0.82, fontSize: 19, color: C.ink, align: 'center', margin: 0, fit: 'shrink' });
}

// 7 — Alertas iniciales
{
  const s = baseSlide('Detección inicial: 6 alertas', 'Evidencia');
  const img = path.resolve('C:/Users/Inicib/AppData/Local/Temp/codex-clipboard-2fe00bbe-eedf-4b74-ac5f-bf0079a28b90.png');
  s.addImage({ path: img, x: 0.72, y: 1.35, w: 6.0, h: 5.25 });
  addMetric(s, '6', 'alertas publicadas', 7.15, 1.55, C.red);
  addMetric(s, '3', 'problemas únicos', 9.25, 1.55, C.teal);
  s.addText('Alertas superpuestas', { x: 7.2, y: 3.2, w: 4.2, h: 0.32, fontSize: 17, bold: true, color: C.navy, margin: 0 });
  addBulletList(s, [
    'eval: consulta propia, CodeQL estándar y Semgrep',
    'SQL injection: CodeQL estándar y Semgrep',
    'Falta de rate limiting: CodeQL estándar'
  ], 7.2, 3.75, 4.85, 2.0, 15.5);
  s.addText('Una alerta no equivale necesariamente a una vulnerabilidad distinta.', { x: 7.2, y: 5.9, w: 4.8, h: 0.55, fontSize: 15.5, italic: true, color: C.muted, margin: 0, fit: 'shrink' });
}

// 8 — QL personalizada
{
  const s = baseSlide('Consulta QL personalizada', 'Implementación');
  addCode(s, 'DangerousEval.ql', [
    '/** @kind problem',
    ' *  @id grupo3/js-dangerous-eval */',
    'import javascript',
    '',
    'from CallExpr call',
    'where call.getCalleeName() = "eval"',
    'select call, "Se ejecuta texto mediante eval"'
  ], 0.78, 1.55, 6.45, 4.65, C.teal);
  const parts = [
    ['from', 'declara el elemento'],
    ['where', 'filtra llamadas a eval'],
    ['select', 'ubica y explica la alerta']
  ];
  parts.forEach((p, i) => {
    const y = 1.75 + i * 1.35;
    addLabel(s, p[0], 8.0, y, 1.2, i === 2 ? C.green : C.teal);
    s.addText(p[1], { x: 9.45, y: y + 0.01, w: 2.6, h: 0.34, fontSize: 16, color: C.ink, margin: 0, fit: 'shrink' });
  });
  s.addText('Se mantuvo abierta por diseño para demostrar la consulta. El endpoint está deshabilitado por defecto.', { x: 7.95, y: 5.45, w: 4.35, h: 0.74, fontSize: 15.5, color: C.muted, margin: 0, fit: 'shrink' });
}

// 9 — Semgrep
{
  const s = baseSlide('Semgrep como segunda fuente de evidencia', 'Integración');
  s.addText('Reglas locales en YAML', { x: 0.88, y: 1.52, w: 3.3, h: 0.38, fontSize: 20, bold: true, color: C.navy, margin: 0 });
  addBulletList(s, [
    'grupo3.javascript.sql-concatenado',
    'grupo3.javascript.eval',
    'Ejecución en GitHub Actions',
    'Salida SARIF visible en Code scanning'
  ], 0.92, 2.15, 5.4, 2.65, 17);
  addCode(s, 'Comando del workflow', [
    'semgrep scan --config semgrep.yml',
    '  --sarif --output semgrep.sarif src',
    '',
    'github/codeql-action/upload-sarif@v4'
  ], 6.82, 1.85, 5.55, 2.2, C.teal);
  s.addShape(pptx.ShapeType.roundRect, { x: 6.82, y: 4.65, w: 5.55, h: 1.22, rectRadius: 0.04, fill: { color: C.pale }, line: { color: C.line } });
  s.addText('Resultado', { x: 7.12, y: 4.93, w: 1.15, h: 0.25, fontSize: 14, bold: true, color: C.teal, margin: 0 });
  s.addText('retroalimentación rápida y reglas fáciles de adaptar al proyecto', { x: 8.35, y: 4.85, w: 3.65, h: 0.46, fontSize: 15.5, color: C.ink, margin: 0, fit: 'shrink' });
}

// 10 — Autofix
{
  const s = baseSlide('Copilot Autofix: propuesta y revisión', 'Corrección');
  addCode(s, 'ANTES', [
    'const sql = "SELECT ... WHERE category = \'"',
    '  + category + "\' ORDER BY name";',
    'await pool.query(sql);'
  ], 0.78, 1.72, 5.55, 2.15, C.red);
  addCode(s, 'DESPUÉS', [
    'const sql = "SELECT ... WHERE category = $1',
    '  ORDER BY name";',
    'await pool.query(sql, [category]);'
  ], 7.0, 1.72, 5.55, 2.15, C.green);
  s.addShape(pptx.ShapeType.chevron, { x: 6.42, y: 2.45, w: 0.44, h: 0.58, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText('Qué cambia', { x: 0.9, y: 4.55, w: 2.0, h: 0.32, fontSize: 17, bold: true, color: C.navy, margin: 0 });
  addBulletList(s, [
    'El comando SQL queda separado del valor externo.',
    'PostgreSQL recibe el dato en el marcador $1.',
    'El equipo revisa el diff y confirma el comportamiento con pruebas.'
  ], 0.92, 5.0, 11.1, 1.3, 16.5);
}

// 11 — PR validation
{
  const s = baseSlide('El pull request también encontró errores', 'Validación');
  const img = path.resolve('C:/Users/Inicib/AppData/Local/Temp/codex-clipboard-bf555776-0189-4730-9744-a3ea76f1a8b6.png');
  s.addImage({ path: img, x: 0.72, y: 1.38, w: 7.15, h: 4.75 });
  s.addText('1', { x: 8.35, y: 1.55, w: 0.55, h: 0.55, fontSize: 22, bold: true, color: C.white, align: 'center', margin: 0, fill: { color: C.red } });
  s.addText('La prueba antigua esperaba el texto de ataque dentro del SQL.', { x: 9.05, y: 1.55, w: 3.15, h: 0.62, fontSize: 15.5, color: C.ink, margin: 0, fit: 'shrink' });
  s.addText('2', { x: 8.35, y: 2.85, w: 0.55, h: 0.55, fontSize: 22, bold: true, color: C.white, align: 'center', margin: 0, fill: { color: C.teal } });
  s.addText('El grupo cambió la prueba para validar dos argumentos en pool.query.', { x: 9.05, y: 2.85, w: 3.15, h: 0.62, fontSize: 15.5, color: C.ink, margin: 0, fit: 'shrink' });
  s.addText('3', { x: 8.35, y: 4.15, w: 0.55, h: 0.55, fontSize: 22, bold: true, color: C.white, align: 'center', margin: 0, fill: { color: C.green } });
  s.addText('Un nuevo análisis detectó falta de rate limiting antes de fusionar.', { x: 9.05, y: 4.15, w: 3.15, h: 0.62, fontSize: 15.5, color: C.ink, margin: 0, fit: 'shrink' });
  s.addText('Autofix propone; el equipo verifica.', { x: 8.38, y: 5.65, w: 3.75, h: 0.35, fontSize: 17, bold: true, italic: true, color: C.navy, align: 'center', margin: 0 });
}

// 12 — Rate limiting
{
  const s = baseSlide('Segunda contramedida: rate limiting', 'Hardening');
  addCode(s, 'Control incorporado', [
    'const limiter = RateLimit({',
    '  windowMs: 60 * 1000,',
    '  max: 30,',
    '  standardHeaders: true,',
    '  legacyHeaders: false',
    '});',
    'app.use(limiter);'
  ], 0.85, 1.55, 5.65, 4.3, C.teal);
  addMetric(s, '30', 'solicitudes por minuto', 7.45, 1.75, C.teal);
  s.addShape(pptx.ShapeType.line, { x: 7.3, y: 3.35, w: 4.55, h: 0, line: { color: C.line, width: 1 } });
  addBulletList(s, [
    'Reduce solicitudes repetidas al acceso de base de datos.',
    'CodeQL dejó de reportar Missing rate limiting.',
    'El control se aplicó antes de fusionar el PR.'
  ], 7.15, 3.85, 5.1, 2.05, 16.5);
}

// 13 — Resultados
{
  const s = baseSlide('Resultados medidos en GitHub Actions', 'Resultados');
  s.addChart(pptx.ChartType.bar, [
    { name: 'CodeQL', labels: ['Inicial', 'Final'], values: [96, 93] },
    { name: 'Semgrep', labels: ['Inicial', 'Final'], values: [38, 25] }
  ], {
    x: 0.82, y: 1.45, w: 7.2, h: 4.8,
    catAxisLabelFontSize: 12, valAxisLabelFontSize: 11,
    valAxisTitle: 'segundos', showValue: true, showLegend: true,
    legendPos: 'b', showTitle: false,
    chartColors: [C.navy, C.teal],
    showCatName: false, showSerName: false,
    gridLine: { color: C.line, width: 1 },
    border: { color: C.line, width: 1 },
    showValue: true
  });
  addMetric(s, '3/3', 'pruebas aprobadas', 8.75, 1.8, C.green);
  addMetric(s, '0', 'vulnerabilidades npm', 10.7, 1.8, C.green);
  s.addText('Estado final', { x: 8.7, y: 3.6, w: 3.65, h: 0.32, fontSize: 17, bold: true, color: C.navy, align: 'center', margin: 0 });
  addBulletList(s, [
    'SQL injection corregido',
    'SQL Semgrep corregido',
    'Rate limiting corregido',
    'eval abierto por diseño'
  ], 8.65, 4.1, 3.9, 1.85, 15.2);
  s.addText('Observaciones del repositorio; no constituyen un benchmark general.', { x: 1.0, y: 6.35, w: 7.0, h: 0.26, fontSize: 10.5, italic: true, color: C.muted, margin: 0 });
}

// 14 — Comparación
{
  const s = baseSlide('CodeQL y Semgrep: roles complementarios', 'Comparación');
  s.addTable([
    [{ text: 'Criterio', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }, { text: 'CodeQL', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }, { text: 'Semgrep', options: { bold: true, color: C.white, fill: C.navy, align: 'center' } }],
    ['Modelo', 'Base de datos semántica y consultas QL', 'Patrones estructurales YAML'],
    ['Flujo de datos', 'Fuente, propagación y sumidero', 'Regla local sintáctica'],
    ['Tiempo inicial', '96 segundos', '38 segundos'],
    ['Consulta propia', 'DangerousEval.ql', '2 reglas en semgrep.yml'],
    ['Corrección asistida', 'Copilot Autofix compatible', 'No se usó Autofix'],
    ['Hallazgo adicional', 'Missing rate limiting', 'No cubierto por reglas locales']
  ], {
    x: 0.72, y: 1.35, w: 11.9, h: 4.65,
    border: { type: 'solid', pt: 1, color: C.line },
    fill: C.white, color: C.ink, fontSize: 12.5,
    rowH: 0.61, margin: 0.08,
    colW: [2.15, 4.9, 4.85], autoFit: false
  });
  s.addText('Conclusión: Semgrep aporta velocidad; CodeQL agrega profundidad semántica y contexto.', { x: 1.05, y: 6.25, w: 11.2, h: 0.38, fontSize: 18, bold: true, color: C.teal, align: 'center', margin: 0, fit: 'shrink' });
}

// 15 — Demo
{
  const s = baseSlide('Plan de demostración — 15 minutos', 'Exposición');
  const segments = [
    ['0–1:30', 'Objetivo'], ['1:30–3:30', 'Código vulnerable'], ['3:30–6:00', 'Alertas'],
    ['6:00–8:00', 'QL propia'], ['8:00–10:30', 'Autofix'], ['10:30–12:30', 'Pruebas'],
    ['12:30–14:00', 'Comparación'], ['14:00–15:00', 'Cierre']
  ];
  segments.forEach((seg, i) => {
    const row = i < 4 ? 0 : 1;
    const col = i % 4;
    const x = 0.72 + col * 3.12;
    const y = 1.55 + row * 2.25;
    const color = i === 4 ? C.teal : (i === 7 ? C.green : C.navy);
    s.addShape(pptx.ShapeType.roundRect, { x, y, w: 2.72, h: 1.55, rectRadius: 0.05, fill: { color: C.white }, line: { color, width: 2 } });
    s.addText(seg[0], { x: x + 0.15, y: y + 0.25, w: 2.42, h: 0.25, fontSize: 11.5, bold: true, color, margin: 0 });
    s.addText(seg[1], { x: x + 0.15, y: y + 0.73, w: 2.42, h: 0.42, fontSize: 16, bold: true, color: C.ink, align: 'center', margin: 0, fit: 'shrink' });
  });
  s.addText('Respaldo: video de 12–15 minutos en 1080p siguiendo el mismo recorrido.', { x: 1.05, y: 6.25, w: 11.15, h: 0.38, fontSize: 17.5, color: C.muted, align: 'center', margin: 0 });
}

// 16 — Cierre
{
  const s = pptx.addSlide();
  s.background = { color: C.navy2 };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.2, h: H, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText('Conclusiones', { x: 0.82, y: 0.72, w: 4.3, h: 0.62, fontFace: 'Aptos Display', fontSize: 33, bold: true, color: C.white, margin: 0 });
  addBulletList(s, [
    'El pipeline detectó seis alertas que correspondían a tres problemas únicos.',
    'Copilot Autofix propuso un SQL parametrizado, pero el equipo validó y completó el parche.',
    'CodeQL añadió contexto de flujo y encontró la falta de rate limiting.',
    'Semgrep fue más rápido y útil para reglas locales sencillas.',
    'La combinación de herramientas mejoró la detección y la revisión.'
  ], 0.92, 1.75, 8.25, 3.85, 18, 'E7EEF2');
  s.addShape(pptx.ShapeType.roundRect, { x: 9.55, y: 1.55, w: 2.65, h: 2.65, rectRadius: 0.08, fill: { color: C.teal, transparency: 12 }, line: { color: '7DD3D1', width: 1.5 } });
  s.addText('¿Preguntas?', { x: 9.75, y: 2.45, w: 2.25, h: 0.55, fontSize: 25, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('github.com/ChethhSito/CodeQL_Copilot', { x: 0.92, y: 6.35, w: 5.9, h: 0.3, fontSize: 13, color: '9CB4C0', margin: 0 });
  s.addText('Grupo 3', { x: 10.2, y: 6.35, w: 2, h: 0.3, fontSize: 13, bold: true, color: C.white, align: 'right', margin: 0 });
}

const output = path.resolve(process.argv[2] || 'entregables/Presentacion_CodeQL_Copilot_Autofix_Grupo3.pptx');
pptx.writeFile({ fileName: output });

