#!/usr/bin/env python3
"""Build LineGuide_Proposal_v2.2.0.pptx and .pdf from deck-content.json.

Clean-room port of revisions/v2.1.0/source/build-deck.mjs layout semantics using
only public tooling (python-pptx + reportlab). Both backends render from the same
coordinates, so the committed PDF is a faithful render of the same layout data.
Emits overflow warnings during build.
"""
import json, pathlib, os, math

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = pathlib.Path(os.environ.get("LINEGUIDE_OUT", ROOT / "artifact"))
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
INK, MUTED, TEAL, RULE, PAPER, WHITE = "#0B2133", "#405B68", "#006D77", "#CAD5DB", "#FAFCFC", "#FFFFFF"
FONT = "Arial"
WARN = []

content = json.loads((HERE / "deck-content.json").read_text())

# ------------------------------------------------------------------ PDF backend
from reportlab.pdfgen import canvas as rl
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

def hc(c): return HexColor(c)

class Pdf:
    def __init__(self, path): self.c = rl.Canvas(str(path), pagesize=(W, H))
    def page(self):
        self.c.setFillColor(hc(PAPER)); self.c.rect(0, 0, W, H, stroke=0, fill=1)
    def done(self): self.c.showPage()
    def save(self): self.c.save()
    def wrap(self, t, size, w, bold=False):
        f = "Helvetica-Bold" if bold else "Helvetica"
        lines = []
        for para in str(t).split("\n"):
            words, cur = para.split(" "), ""
            for wd in words:
                trial = (cur + " " + wd).strip()
                if stringWidth(trial, f, size) <= w: cur = trial
                else:
                    if cur: lines.append(cur)
                    cur = wd
            lines.append(cur)
        return lines
    def text(self, t, x, y, w, h, size=26, color=INK, bold=False, name="text", link=None, bg=None):
        if bg:
            self.c.setFillColor(hc(bg)); self.c.rect(x, H - y - h, w, h, stroke=0, fill=1)
        lines = self.wrap(t, size, w, bold)
        lh = size * 1.28
        if len(lines) * lh > h + 2: WARN.append(f"PDF overflow [{name}]: {len(lines)}x{lh:.0f}>{h} :: {str(t)[:60]!r}")
        self.c.setFillColor(hc(color)); self.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        ty = H - y - size
        for ln in lines:
            self.c.drawString(x, ty, ln)
            if link: self.c.linkURL(link, (x, ty - 2, x + stringWidth(ln, "Helvetica", size), ty + size), relative=0)
            ty -= lh
    def line(self, x1, y1, x2, y2, color=RULE, width=1, dashed=False, arrow=False):
        self.c.setStrokeColor(hc(color)); self.c.setLineWidth(width)
        if dashed: self.c.setDash(4, 3)
        self.c.line(x1, H - y1, x2, H - y2)
        if dashed: self.c.setDash()
        if arrow:
            ang = math.atan2(-(y2 - y1), x2 - x1); a = 9
            p = self.c.beginPath()
            p.moveTo(x2, H - y2)
            p.lineTo(x2 - a * math.cos(ang - 0.42), H - y2 + a * math.sin(ang - 0.42))
            p.lineTo(x2 - a * math.cos(ang + 0.42), H - y2 + a * math.sin(ang + 0.42))
            p.close(); self.c.setFillColor(hc(color)); self.c.drawPath(p, stroke=0, fill=1)
    def rect(self, x, y, w, h, fill=WHITE, stroke=TEAL, sw=1.6, dashed=False):
        self.c.setFillColor(hc(fill)); self.c.setStrokeColor(hc(stroke)); self.c.setLineWidth(sw)
        if dashed: self.c.setDash(4, 3)
        self.c.rect(x, H - y - h, w, h, stroke=1, fill=1)
        if dashed: self.c.setDash()

# ----------------------------------------------------------------- PPTX backend
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, MSO_ANCHOR, PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

E = lambda px: Emu(int(px * 9525))
def rgb(c): return RGBColor.from_string(c.lstrip("#"))

class Pptx:
    def __init__(self):
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = E(W), E(H)
        self.blank = self.p.slide_layouts[6]
    def page(self):
        s = self.p.slides.add_slide(self.blank)
        s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(PAPER)
        return s
    def save(self, path): self.p.save(str(path))
    @staticmethod
    def text(s, t, x, y, w, h, size=26, color=INK, bold=False, name="text", link=None, bg=None):
        tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tb.name = name
        if bg:
            tb.fill.solid(); tb.fill.fore_color.rgb = rgb(bg)
        tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_ANCHOR.TOP
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
        for i, para in enumerate(str(t).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run(); r.text = para
            r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(color)
            if link: r.hyperlink.address = link
    @staticmethod
    def line(s, x1, y1, x2, y2, color=RULE, width=1, dashed=False, arrow=False):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
        ln.line.color.rgb = rgb(color); ln.line.width = Pt(width)
        lnEl = ln.line._get_or_add_ln()
        if dashed: lnEl.insert(0, lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}))
        if arrow: lnEl.append(lnEl.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'sm', 'len': 'sm'}))
    @staticmethod
    def rect(s, x, y, w, h, fill=WHITE, stroke=TEAL, sw=1.6, dashed=False):
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        sh.line.color.rgb = rgb(stroke); sh.line.width = Pt(sw)
        if dashed:
            lnEl = sh.line._get_or_add_ln()
            lnEl.insert(0, lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}))
        sh.shadow.inherit = False

KIND = None
def T(s, t, x, y, w, h, size=26, color=INK, bold=False, name="text", link=None, bg=None):
    if KIND == "pdf": PDF.text(t, x, y, w, h, size, color, bold, name, link, bg)
    else: Pptx.text(s, t, x, y, w, h, size, color, bold, name, link, bg)
def L(s, x1, y1, x2, y2, color=RULE, width=1, dashed=False, arrow=False):
    if KIND == "pdf": PDF.line(x1, y1, x2, y2, color, width, dashed, arrow)
    else: Pptx.line(s, x1, y1, x2, y2, color, width, dashed, arrow)
def R(s, x, y, w, h, fill=WHITE, stroke=TEAL, sw=1.6, dashed=False):
    if KIND == "pdf": PDF.rect(x, y, w, h, fill, stroke, sw, dashed)
    else: Pptx.rect(s, x, y, w, h, fill, stroke, sw, dashed)

def base(d, i):
    s = PDF.page() if KIND == "pdf" else PPT.page()
    if d["type"] != "cover":
        T(s, d["title"], 64, 38, 1152, 98, d.get("titleFontSize", 44), INK, True, "slide-title")
    L(s, 64, 660, 1216, 660)
    T(s, d.get("footer", "Hypothetical proposal. Proposed targets remain unmeasured."),
      64, 676, 1080, 24, 15, MUTED, name="footer")
    T(s, str(i + 1).zfill(2), 1176, 674, 40, 28, 18, MUTED, name="slide-number")
    return s

def table(s, d):
    top, height, fs = d.get("top", 156), d.get("height", 428), d.get("fontSize", 24)
    vals = [d["headers"], *d["rows"]]
    nr, nc = len(vals), len(d["headers"])
    if KIND == "pdf":
        xs = [64]
        for wd in d["widths"]: xs.append(xs[-1] + wd)
        rh = height / nr
        for r in range(nr):
            ry = top + r * rh
            PDF.c.setFillColor(hc(INK if r == 0 else (WHITE if r % 2 else "#EFF4F5")))
            PDF.c.rect(64, H - ry - rh, 1152, rh, stroke=0, fill=1)
            for ci in range(nc):
                cell = str(vals[r][ci])
                lines = PDF.wrap(cell, fs, d["widths"][ci] - 24, bold=(r == 0))
                lh = fs * 1.24
                if len(lines) * lh > rh - 10: WARN.append(f"PDF overflow [table r{r}c{ci}]: {cell[:50]!r}")
                PDF.c.setFillColor(hc(WHITE if r == 0 else INK))
                PDF.c.setFont("Helvetica-Bold" if r == 0 else "Helvetica", fs)
                ty = H - ry - rh / 2 + len(lines) * lh / 2 - fs
                for ln in lines:
                    PDF.c.drawString(xs[ci] + 12, ty, ln); ty -= lh
        PDF.c.setStrokeColor(hc(RULE)); PDF.c.setLineWidth(0.75)
        for r in range(nr + 1): PDF.c.line(64, H - top - r * rh, 1216, H - top - r * rh)
        for x in xs: PDF.c.line(x, H - top, x, H - top - height)
    else:
        shp = s.shapes.add_table(nr, nc, E(64), E(top), E(1152), E(height))
        t = shp.table
        for ci, wd in enumerate(d["widths"]): t.columns[ci].width = E(wd)
        for r in range(nr):
            t.rows[r].height = E(height / nr)
            for ci in range(nc):
                cell = t.cell(r, ci)
                cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (WHITE if r % 2 else "#EFF4F5"))
                cell.margin_left = cell.margin_right = E(12)
                cell.margin_top = cell.margin_bottom = E(7)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = cell.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; run = p.add_run(); run.text = str(vals[r][ci])
                f = run.font; f.size = Pt(fs); f.bold = (r == 0); f.name = FONT
                f.color.rgb = rgb(WHITE if r == 0 else INK)
    if d.get("caption"):
        T(s, d["caption"], 64, d.get("captionTop", 610), 1152, 44, 20, MUTED, name="caption")

def rows(s, d):
    top, gap = d.get("top", 156), d.get("gap", 108)
    lw, dx = d.get("labelWidth", 290), d.get("detailX", 380)
    for j, r in enumerate(d["rows"]):
        T(s, r[0], 64, top + j * gap, lw, gap - 16, d.get("labelFontSize", 27), TEAL, True, "row-label")
        T(s, r[1], dx, top + j * gap, 1216 - dx, gap - 16, d.get("fontSize", 26), name="row-detail")
        if j < len(d["rows"]) - 1: L(s, 64, top + j * gap + gap - 15, 1216, top + j * gap + gap - 15)
    if d.get("caption"):
        T(s, d["caption"], 64, d.get("captionTop", 608), 1152, 44, 20, MUTED, name="caption")

def two(s, d):
    T(s, d["leftTitle"], 64, 158, 530, 52, 29, TEAL, True, "left-title")
    T(s, d["rightTitle"], 670, 158, 546, 52, 29, TEAL, True, "right-title")
    T(s, d["left"], 64, 226, 530, 365, d.get("fontSize", 27), name="left-body")
    T(s, d["right"], 670, 226, 546, 365, d.get("fontSize", 27), name="right-body")
    if d.get("caption"):
        T(s, d["caption"], 64, d.get("captionTop", 611), 1152, 42, 20, MUTED, name="caption")

def statement(s, d):
    if d.get("definitionLabel"):
        T(s, d["definitionLabel"], 64, 148, 1152, 36, 23, MUTED, True, "definition-label")
    T(s, d["statement"], 64, d.get("statementTop", 174), 1140, d.get("statementHeight", 230),
      d.get("statementFontSize", 42), TEAL, True, "main-statement")
    T(s, d["body"], 64, d.get("bodyTop", 438), 1140, d.get("bodyHeight", 176),
      d.get("bodyFontSize", 27), name="statement-body")

def sources(s, d):
    gap = d.get("sourceGap", 80 if len(d["ids"]) > 5 else 92)
    base_size = d.get("sourceFontSize", 22 if len(d["ids"]) > 5 else 25)
    for j, sid in enumerate(d["ids"]):
        z = next(x for x in content["sources"] if x["id"] == sid)
        y = 148 + j * gap
        ts = min(base_size, 20) if len(z["title"]) > 85 else base_size
        T(s, f"{sid}  {z['title']}", 64, y, 1152, 36, ts, INK, True, "source-title")
        u = z["url"]
        us = 14 if len(u) > 150 else (16 if len(u) > 95 else 19)
        T(s, u, 64, y + 38, 1152, 45, us, TEAL, name="source-url", link=u)

def NT(s, t, x, y, w, h, size=23, bold=False):
    """Node label: horizontally centered, vertically middle (matches v2.1.0 style)."""
    if KIND == "pdf":
        lines = PDF.wrap(t, size, w - 16, bold)
        lh = size * 1.22
        total = len(lines) * lh
        if total > h - 4: WARN.append(f"PDF overflow [node]: {str(t)[:50]!r}")
        PDF.c.setFillColor(hc(INK)); PDF.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        ty = H - y - h / 2 + total / 2 - size
        for ln in lines:
            PDF.c.drawCentredString(x + w / 2, ty, ln); ty -= lh
    else:
        tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tb.name = "node-label"
        tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, E(8))
        for i, para in enumerate(str(t).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = para
            r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(INK)

def diagram(s, d):
    for b in d.get("boundaries", []):
        R(s, b["x"], b["y"], b["w"], b["h"], fill=PAPER, stroke=b.get("color", MUTED), sw=1.25, dashed=True)
        wraps = b["w"] < 300 and len(b["label"]) > 27
        T(s, b["label"], b["x"] + 8, b["y"] - (45 if wraps else 27), b["w"] - 16,
          42 if wraps else 26, b.get("fontSize", 16 if b["w"] < 300 else 18), MUTED, True, "boundary-label")
    for e in d.get("edges", []):
        pts = e["points"]
        for j in range(1, len(pts)):
            last = j == len(pts) - 1
            L(s, pts[j - 1][0], pts[j - 1][1], pts[j][0], pts[j][1],
              color=e.get("color", TEAL), width=e.get("width", 2), dashed=e.get("dashed", False), arrow=last)
    for n in d.get("nodes", []):
        R(s, n["x"], n["y"], n["w"], n["h"], fill=n.get("fill", WHITE), stroke=n.get("color", TEAL), sw=1.6)
        NT(s, n["label"], n["x"], n["y"], n["w"], n["h"], n.get("fontSize", 23), n.get("bold", False))
    for e in d.get("edges", []):
        if e.get("label"):
            T(s, e["label"], e.get("labelX", 0), e.get("labelY", 0), e.get("labelW", 170),
              e.get("labelH", 20), e.get("labelFontSize", e.get("fontSize", 16)), MUTED, name="flow-label", bg=PAPER)
    for a in d.get("annotations", []):
        T(s, a["text"], a["x"], a["y"], a["w"], a.get("h", 44), a.get("fontSize", 19),
          a.get("color", MUTED), a.get("bold", False), "diagram-annotation")
    if d.get("caption"):
        T(s, d["caption"], 64, d.get("captionTop", 607), 1152, d.get("captionHeight", 44),
          d.get("captionFontSize", 19), INK, name="diagram-caption")

def notes(s, d):
    refs = []
    for sid in d.get("sources", []):
        z = next((x for x in content["sources"] if x["id"] == sid), None)
        if z: refs.append(f"{sid}: {z['title']}\n{z['url']}\nSource limit: {z.get('limit', 'See the versioned source register.')}")
    body = "\n\n".join(x for x in [
        d.get("notes", ""),
        f"Evidence status: {d.get('status', 'Design proposal. No operational model test, user study or deployment has been run.')}",
        "References:\n" + "\n\n".join(refs) if refs else "",
    ] if x)
    if KIND == "pptx":
        s.notes_slide.notes_text_frame.text = body

# --------------------------------------------------------------------- build
for kind in ("pdf", "pptx"):
    KIND = kind
    if kind == "pdf": PDF = Pdf(OUT / "LineGuide_Proposal_v2.2.0.pdf")
    else: PPT = Pptx()
    for i, d in enumerate(content["slides"]):
        s = base(d, i)
        ty = d["type"]
        if ty == "cover":
            T(s, "LineGuide", 64, 120, 1152, 110, 80, INK, True, "cover-title")
            T(s, d.get("subtitle", "AI-powered industrial robot\nexpert advisor"), 64, 260, 1100, 160, 48, TEAL, name="cover-subtitle")
            T(s, d.get("meta", ""), 64, 494, 1100, 110, 27, MUTED, name="cover-meta")
        elif ty == "table": table(s, d)
        elif ty == "rows": rows(s, d)
        elif ty == "two": two(s, d)
        elif ty == "statement": statement(s, d)
        elif ty == "sources": sources(s, d)
        elif ty == "diagram": diagram(s, d)
        else: raise ValueError("Unsupported layout " + ty)
        notes(s, d)
        if kind == "pdf": PDF.done()
    if kind == "pdf": PDF.save()
    else: PPT.save(OUT / "LineGuide_Proposal_v2.2.0.pptx")
    print(kind.upper(), "written")

if WARN:
    print("\nLAYOUT WARNINGS:"); [print(" -", w) for w in WARN]
else:
    print("No layout warnings.")
