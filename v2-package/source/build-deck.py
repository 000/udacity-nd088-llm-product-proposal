#!/usr/bin/env python3
"""Build LineGuide_Proposal_v2.pptx and .pdf from deck-content-v2.json.

Single layout engine, two backends (python-pptx and reportlab) so the PDF is a
faithful render of the same coordinates. Emits overflow warnings during build.
"""
import json, pathlib, sys, os

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = pathlib.Path(os.environ.get("LINEGUIDE_OUT", ROOT / "dist"))
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
INK, MUTED, TEAL, ACCENT, RULE, PAPER = "#0B2133", "#405B68", "#006D77", "#B34E22", "#CAD5DB", "#FAFCFC"
FONT = "Arial"
WARNINGS = []

content = json.loads((HERE / os.environ.get("LINEGUIDE_CONTENT", "deck-content.json")).read_text())

# ---------------------------------------------------------------- PDF backend
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

def hexcol(c): return HexColor(c)

class Pdf:
    def __init__(self, path):
        self.c = rl_canvas.Canvas(str(path), pagesize=(W, H))
    def page(self, bg=PAPER):
        self.c.setFillColor(hexcol(bg)); self.c.rect(0, 0, W, H, stroke=0, fill=1)
    def save(self): self.c.showPage(); self.c.save()
    def wrap(self, text, size, width, bold=False):
        f = "Helvetica-Bold" if bold else "Helvetica"
        lines = []
        for para in text.split("\n"):
            words, cur = para.split(" "), ""
            for w_ in words:
                t = (cur + " " + w_).strip()
                if stringWidth(t, f, size) <= width: cur = t
                else:
                    if cur: lines.append(cur)
                    cur = w_
            lines.append(cur)
        return lines
    def text(self, t, x, y, w, h, size=25, color=INK, bold=False, name="text", link=None):
        lines = self.wrap(t, size, w, bold)
        lh = size * 1.28
        if len(lines) * lh > h + 2:
            WARNINGS.append(f"PDF overflow [{name}]: {len(lines)} lines x {lh:.0f}pt > {h}pt :: {t[:60]!r}")
        self.c.setFillColor(hexcol(color)); self.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        ty = H - y - size  # top-anchored
        for ln in lines:
            self.c.drawString(x, ty, ln)
            if link: self.c.linkURL(link, (x, ty - 3, x + stringWidth(ln, "Helvetica", size), ty + size), relative=0)
            ty -= lh
    def hline(self, x, y, w, color=RULE, width=1, dash=None):
        self.c.setStrokeColor(hexcol(color)); self.c.setLineWidth(width)
        if dash: self.c.setDash(*dash)
        self.c.line(x, H - y, x + w, H - y)
        if dash: self.c.setDash()
    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=TEAL, sw=1.5, text=None, size=23, dash=None):
        self.c.setFillColor(hexcol(fill)); self.c.setStrokeColor(hexcol(stroke)); self.c.setLineWidth(sw)
        if dash: self.c.setDash(*dash)
        self.c.rect(x, H - y - h, w, h, stroke=1, fill=1)
        if dash: self.c.setDash()
        if text is not None:
            lines = self.wrap(text, size, w - 20)
            lh = size * 1.22
            total = len(lines) * lh
            if total > h - 6: WARNINGS.append(f"PDF overflow [node]: {text[:50]!r}")
            self.c.setFillColor(hexcol(INK)); self.c.setFont("Helvetica", size)
            ty = H - y - h / 2 + total / 2 - size
            for ln in lines:
                self.c.drawCentredString(x + w / 2, ty, ln); ty -= lh
    def arrow(self, x1, y1, x2, y2, color=TEAL, width=2, dash=None):
        import math
        self.c.setStrokeColor(hexcol(color)); self.c.setLineWidth(width)
        if dash: self.c.setDash(*dash)
        self.c.line(x1, H - y1, x2, H - y2)
        if dash: self.c.setDash()
        ang = math.atan2(-(y2 - y1), x2 - x1)
        a = 9
        p1 = (x2, H - y2)
        p2 = (x2 - a * math.cos(ang - 0.42), H - y2 + a * math.sin(ang - 0.42))
        p3 = (x2 - a * math.cos(ang + 0.42), H - y2 + a * math.sin(ang + 0.42))
        self.c.setFillColor(hexcol(color))
        path = self.c.beginPath(); path.moveTo(*p1); path.lineTo(*p2); path.lineTo(*p3); path.close()
        self.c.drawPath(path, stroke=0, fill=1)

# --------------------------------------------------------------- PPTX backend
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
    def slide(self, bg=PAPER):
        s = self.p.slides.add_slide(self.blank)
        s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(bg)
        return s
    def save(self, path): self.p.save(str(path))
    @staticmethod
    def text(s, t, x, y, w, h, size=25, color=INK, bold=False, name="text", link=None):
        tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tb.name = name
        tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_ANCHOR.TOP
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
        for i, para in enumerate(t.split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run(); r.text = para
            r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT
            r.font.color.rgb = rgb(color)
            if link: r.hyperlink.address = link
    @staticmethod
    def hline(s, x, y, w, color=RULE, width=1.0, dash=None):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x), E(y), E(x + w), E(y))
        ln.line.color.rgb = rgb(color); ln.line.width = Pt(width)
        if dash:
            lnEl = ln.line._get_or_add_ln()
            d = lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}); lnEl.append(d)
    @staticmethod
    def rect(s, x, y, w, h, fill="#FFFFFF", stroke=TEAL, sw=1.5, text=None, size=23, dash=None):
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        sh.line.color.rgb = rgb(stroke); sh.line.width = Pt(sw)
        if dash:
            lnEl = sh.line._get_or_add_ln()
            d = lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}); lnEl.append(d)
        sh.shadow.inherit = False
        if text is not None:
            tf = sh.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            for i, para in enumerate(text.split("\n")):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run(); r.text = para
                r.font.size = Pt(size); r.font.name = FONT; r.font.color.rgb = rgb(INK)
    @staticmethod
    def arrow(s, x1, y1, x2, y2, color=TEAL, width=2.0, dash=None):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
        ln.line.color.rgb = rgb(color); ln.line.width = Pt(width)
        lnEl = ln.line._get_or_add_ln()
        tail = lnEl.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'sm', 'len': 'sm'})
        lnEl.append(tail)
        if dash:
            d = lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}); lnEl.insert(0, d)

# ------------------------------------------------------------- shared layouts
class Deck:
    def __init__(self, kind):
        self.kind = kind
        self.backend = Pptx() if kind == "pptx" else Pdf(OUT / "LineGuide_Proposal_v2.pdf")
    def new_slide(self):
        return self.backend.slide() if self.kind == "pptx" else None
    def text(self, s, *a, **k):
        (Pptx.text if self.kind == "pptx" else self.backend.text)(s, *a, **k) if self.kind == "pptx" else self.backend.text(*a, **k)
    def finish_page(self, pdfctx):
        if self.kind == "pdf": self.backend.c.showPage()

def base(d, i):
    s = deck.new_slide()
    if deck.kind == "pdf":
        deck.backend.page()
        b = deck.backend
        if d["type"] != "cover":
            b.text(d["title"], 64, 42, 1152, 96, 44, INK, True)
        b.hline(64, 660, 1152)
        b.text(d.get("footer", "Hypothetical product proposal \u2022 Proposed targets are unmeasured"), 64, 677, 1080, 24, 15, MUTED)
        b.text(str(i + 1).zfill(2), 1174, 675, 42, 26, 17, MUTED)
    else:
        if d["type"] != "cover":
            deck.text(s, d["title"], 64, 42, 1152, 96, 44, INK, True, "slide-title")
        Pptx.hline(s, 64, 660, 1152)
        deck.text(s, d.get("footer", "Hypothetical product proposal \u2022 Proposed targets are unmeasured"), 64, 677, 1080, 24, 15, MUTED, name="footer")
        deck.text(s, str(i + 1).zfill(2), 1174, 675, 42, 26, 17, MUTED, name="slide-number")
    return s

def T(s, t, x, y, w, h, size=25, color=INK, bold=False, name="text", link=None):
    if deck.kind == "pdf": deck.backend.text(t, x, y, w, h, size, color, bold, name, link)
    else: Pptx.text(s, t, x, y, w, h, size, color, bold, name, link)

def table(s, d):
    top, height = d.get("top", 156), d.get("height", 440)
    vals = [d["headers"], *d["rows"]]
    ncol, nrow = len(d["headers"]), len(vals)
    fs = d.get("fontSize", 23)
    if deck.kind == "pdf":
        b = deck.backend
        xs = [64]
        for wd in d["widths"]: xs.append(xs[-1] + wd)
        rh = height / nrow
        for r in range(nrow):
            ry = top + r * rh
            b.c.setFillColor(hexcol(INK if r == 0 else ("#FFFFFF" if r % 2 else "#EFF4F5")))
            b.c.rect(64, H - ry - rh, 1152, rh, stroke=0, fill=1)
            for ci in range(ncol):
                cell = str(vals[r][ci])
                lines = b.wrap(cell, fs, d["widths"][ci] - 24, bold=(r == 0))
                lh = fs * 1.24
                total = len(lines) * lh
                if total > rh - 8: WARNINGS.append(f"PDF overflow [table r{r}c{ci}]: {cell[:50]!r}")
                b.c.setFillColor(hexcol("#FFFFFF" if r == 0 else INK))
                b.c.setFont("Helvetica-Bold" if r == 0 else "Helvetica", fs)
                ty = H - ry - rh / 2 + total / 2 - fs
                for ln in lines:
                    b.c.drawString(xs[ci] + 12, ty, ln); ty -= lh
        b.c.setStrokeColor(hexcol(RULE)); b.c.setLineWidth(0.65)
        for r in range(nrow + 1): b.c.line(64, H - top - r * rh, 64 + 1152, H - top - r * rh)
        for x in xs: b.c.line(x, H - top, x, H - top - height)
    else:
        shp = s.shapes.add_table(nrow, ncol, E(64), E(top), E(1152), E(height))
        t = shp.table
        for ci, wd in enumerate(d["widths"]): t.columns[ci].width = E(wd)
        for r in range(nrow):
            for ci in range(ncol):
                cell = t.cell(r, ci)
                cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else ("#FFFFFF" if r % 2 else "#EFF4F5"))
                cell.margin_left = cell.margin_right = E(12)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = cell.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; run = p.add_run(); run.text = str(vals[r][ci])
                f = run.font; f.size = Pt(fs); f.bold = (r == 0); f.name = FONT
                f.color.rgb = rgb("#FFFFFF" if r == 0 else INK)
    if d.get("caption"): T(s, d["caption"], 64, 610, 1152, 42, 20, MUTED, name="table-caption")

def rows(s, d):
    top, gap = d.get("top", 156), d.get("gap", 108)
    for j, r in enumerate(d["rows"]):
        T(s, r[0], 64, top + j * gap, 290, gap - 16, 27, TEAL, True, "row-label")
        T(s, r[1], 380, top + j * gap, 836, gap - 16, d.get("fontSize", 26), INK, name="row-detail")
        if j < len(d["rows"]) - 1:
            (deck.backend.hline(64, top + j * gap + gap - 15, 1152) if deck.kind == "pdf"
             else Pptx.hline(s, 64, top + j * gap + gap - 15, 1152))
    if d.get("caption"): T(s, d["caption"], 64, 608, 1152, 40, 20, MUTED, name="row-caption")

def two(s, d):
    T(s, d["leftTitle"], 64, 158, 530, 52, 29, TEAL, True, "left-title")
    T(s, d["rightTitle"], 670, 158, 546, 52, 29, TEAL, True, "right-title")
    T(s, d["left"], 64, 226, 530, 365, d.get("fontSize", 27), name="left-body")
    T(s, d["right"], 670, 226, 546, 365, d.get("fontSize", 27), name="right-body")
    if d.get("caption"): T(s, d["caption"], 64, 611, 1152, 40, 20, MUTED, name="two-caption")

def architecture(s, d):
    b = deck.backend
    pdf = deck.kind == "pdf"
    def label(t, x, y, w, size=16):
        (b.text(t, x, y, w, 24, size, MUTED) if pdf else T(s, t, x, y, w, 24, size, MUTED))
    def node(t, x, y, w, h=82, size=23, dash=None):
        (b.rect(x, y, w, h, text=t, size=size, dash=dash) if pdf else Pptx.rect(s, x, y, w, h, text=t, size=size, dash=dash))
    def coords(n, side):
        return {"right": (n[0] + n[2], n[1] + n[3] / 2), "left": (n[0], n[1] + n[3] / 2),
                "bottom": (n[0] + n[2] / 2, n[1] + n[3]), "top": (n[0] + n[2] / 2, n[1])}[side]
    def arrow(a, bb, fr="right", to="left", dash=None):
        x1, y1 = coords(a, fr); x2, y2 = coords(bb, to)
        (b.arrow(x1, y1, x2, y2, dash=dash) if pdf else Pptx.arrow(s, x1, y1, x2, y2, dash=dash))
    label("Device / public edge", 64, 148, 320, 23)
    (b.text("Private application and data services", 405, 148, 811, 38, 23, MUTED, True) if pdf
     else T(s, "Private application and data services", 405, 148, 811, 38, 23, MUTED, True))
    NA = (64, 218, 240, 90); NB = (374, 218, 255, 90); NC = (699, 218, 247, 90); NE = (1016, 218, 200, 90)
    NF = (1016, 385, 200, 90); NG = (699, 385, 247, 90); CAT = (374, 385, 255, 90); NH = (64, 385, 240, 90)
    AUD = (1016, 514, 200, 72)
    node("Mobile web app\nTechnician + model ID", *NA, size=22)
    node("Entra ID + API\nAuthZ and risk policy", *NB, size=22)
    node("Hybrid retrieval\nTenant + model + revision", *NC, size=22)
    node("Azure OpenAI\nCited draft only", *NE, size=22)
    node("Validation\nCitations + parts", *NF, size=22)
    node("Approved manuals\nBlob + search index", *NG, size=22)
    node("Parts catalogue\nAPI-only SQL lookup", *CAT, size=22)
    node("Human support\nEscalation via API", *NH, size=22)
    node("Audit events\nPseudonymous, filtered", *AUD, size=17, dash=(4, 3))
    arrow(NA, NB); arrow(NB, NC); arrow(NC, NE)
    arrow(NE, NF, "bottom", "top"); arrow(NG, NC, "top", "bottom"); arrow(NB, CAT, "bottom", "top"); arrow(NB, NH, "bottom", "top")
    arrow(NF, AUD, "bottom", "top", dash=(4, 3))
    # catalog -> validation polyline
    if pdf:
        b.hline(501, 475, 0)  # no-op keeps API parity
        b.c.setStrokeColor(hexcol(TEAL)); b.c.setLineWidth(2)
        b.c.line(501, H - 475, 501, H - 510); b.c.line(501, H - 510, 1116, H - 510)
        b.arrow(1116, 510, 1116, 477)
    else:
        Pptx.hline(s, 501, 475, 0, color=TEAL, width=2)
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(501), E(475), E(501), E(510))
        ln.line.color.rgb = rgb(TEAL); ln.line.width = Pt(2)
        ln2 = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(501), E(510), E(1116), E(510))
        ln2.line.color.rgb = rgb(TEAL); ln2.line.width = Pt(2)
        Pptx.arrow(s, 1116, 510, 1116, 477)
    label("Exact catalog records", 700, 481, 310, 23)
    # v2 connection-level security callouts (gate G6)
    if d.get("seclabels"):
        label("TLS 1.3 + authenticated session", 190, 196, 250)
        label("private endpoint, approved region", 826, 192, 250)
        label("read-only SQL", 514, 330, 180)
    # trust boundary
    if pdf:
        b.c.setStrokeColor(hexcol(RULE)); b.c.setLineWidth(1); b.c.setDash(4, 3)
        b.c.line(340, H - 193, 340, H - 493); b.c.setDash()
    else:
        Pptx.hline(s, 340, 193, 0, color=RULE, width=1, dash=True)
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(340), E(193), E(340), E(493))
        ln.line.color.rgb = rgb(RULE); ln.line.width = Pt(1)
        lnEl = ln.line._get_or_add_ln()
        lnEl.insert(0, lnEl.makeelement(qn('a:prstDash'), {'val': 'dash'}))
    label("Trust boundary", 250, 493, 130, 18)
    txt = ("Back-end links use TLS and private endpoints with managed identities; the dashed line is the trust "
           "boundary between the public edge and private services. No network route or credentials reach robot controllers.")
    (b.text(txt, 64, 596, 1152, 58, 19, INK, True) if pdf else T(s, txt, 64, 596, 1152, 58, 19, INK, True, "arch-summary"))

def speaker_notes(s, d):
    cites = "\n\n".join(
        f"{sid}: {z['title']}\n{z['url']}\nLimit: {z.get('limit', 'Vendor documentation establishes features, not application performance.')}"
        for sid in d.get("sources", [])
        for z in [next((x for x in content["sources"] if x["id"] == sid), None)] if z)
    notes = (f"{d.get('notes', '')}\n\nEvidence status: {d.get('status', 'Design proposal; no production deployment or user study has been run.')}"
             f"\n\nSources checked 16 November 2026:\n{cites}")
    if deck.kind == "pptx":
        s.notes_slide.notes_text_frame.text = notes

# ------------------------------------------------------------------ build both
for kind in ("pdf", "pptx"):
    deck = Deck(kind)
    for i, d in enumerate(content["slides"]):
        s = base(d, i)
        ty = d["type"]
        if ty == "cover":
            T(s, "LineGuide", 64, 120, 1152, 110, 80, INK, True, "cover-title")
            T(s, "AI-powered industrial robot\nexpert advisor", 64, 260, 1100, 160, 48, TEAL, name="cover-subtitle")
            T(s, d.get("meta", "Scenario C \u2022 Udacity ND088\nStakeholder proposal \u2022 16 November 2026"),
              64, 494, 1000, 105, 27, MUTED, name="cover-meta")
        elif ty == "table": table(s, d)
        elif ty == "rows": rows(s, d)
        elif ty == "two": two(s, d)
        elif ty == "architecture": architecture(s, d)
        elif ty == "statement":
            T(s, d["statement"], 64, 174, 1140, 230, 42, TEAL, True, "main-statement")
            T(s, d["body"], 64, 438, 1140, 176, 27, name="statement-body")
        elif ty == "sources":
            for j, sid in enumerate(d["ids"]):
                z = next(x for x in content["sources"] if x["id"] == sid)
                yy = 148 + j * 92
                T(s, f"{sid}  {z['title']}", 64, yy, 1152, 34, 25, INK, True)
                u = z["url"]
                ufs = 19 if len(u) <= 95 else (14 if len(u) <= 150 else 12)
                T(s, u, 64, yy + 38, 1152, 45, ufs, TEAL, link=u)
        speaker_notes(s, d)
        if kind == "pdf": deck.backend.c.showPage()
    if kind == "pdf":
        deck.backend.c.save()
        print("PDF written")
    else:
        deck.backend.save(OUT / "LineGuide_Proposal_v2.pptx")
        print("PPTX written")

if WARNINGS:
    print("\nLAYOUT WARNINGS:"); [print(" -", w) for w in WARNINGS]
else:
    print("No layout overflow warnings.")
