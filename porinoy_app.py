"""
PORINOY — Streamlit App (v4)
"""

import json, os, re, time, tempfile, io, base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(page_title="PORINOY", page_icon="📜",
                   layout="wide", initial_sidebar_state="collapsed")

P   = "#EDE7D9"
PD  = "#E3DCC9"
INK = "#1C1B19"
IS  = "#423F38"
RL  = "#C9C2AC"
RU  = "#8B8576"
AC  = "#A13D2B"
ACS = "#C9744F"
GR  = "#5B6B4E"
CA  = "#F6F2E8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ══ HARD RESETS ══ */
html,body{{background:{P}!important;color:{INK}!important;}}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"]
{{background:{P}!important;}}
.main,.main>div{{background:{P}!important;}}


[data-testid="block-container"],
[data-testid="stMainBlockContainer"],
.block-container
{{
  background:{P}!important;
    max-width:1300px !important;
    margin:0 auto !important;
    padding-left:4rem !important;
    padding-right:4rem !important;
    padding-top:0rem !important;
    padding-bottom:0rem !important;
}}

/* Remove the gap Streamlit inserts between every element/section */
[data-testid="stVerticalBlock"]{{gap:0rem!important;}}
[data-testid="element-container"]{{margin:0!important;}}
[data-testid="stElementContainer"]{{margin:0!important;}}

/* Also zero out the column gutters that add extra side space */
#MainMenu,footer,header{{visibility:hidden!important;}}
section[data-testid="stSidebar"]{{display:none!important;}}

/* ══ BASE TEXT ══ */
p,li,td,th,label
{{font-family:'IBM Plex Sans',sans-serif!important;color:{INK}!important;}}
h1,h2,h3,h4
{{font-family:'Source Serif 4',serif!important;color:{INK}!important;font-weight:700!important;}}

/* ══ LAYOUT WRAPPER — our own 24px gutter ══ */
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px;box-sizing:border-box;}}
@media(max-width:700px){{.wrap{{padding:0 14px;}}}}

/* ══ MASTHEAD ══ */
.masthead{{border-bottom:3px solid {INK};padding:18px 90px 12px;background:{P};width:100%;}}
.masthead-inner{{max-width:1120px;margin:0 auto;padding:0 24px;
  display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:10px;}}
.mh-brand{{font-family:'IBM Plex Mono',monospace!important;font-size:11px;
  letter-spacing:.12em;text-transform:uppercase;color:{IS}!important;}}
.mh-nav{{font-family:'IBM Plex Mono',monospace!important;font-size:11px;
  letter-spacing:.08em;color:{IS}!important;}}

/* ══ HERO ══ */
.hero{{padding:64px 90px 56px; background:{P};width:100%;}}
.kicker{{font-family:'IBM Plex Mono',monospace!important;font-size:11px;
  letter-spacing:.16em;text-transform:uppercase;color:{GR}!important;
  display:flex;align-items:center;gap:10px;margin-bottom:18px;}}
.kicker::before{{content:"";width:22px;height:1px;background:{GR};display:inline-block;flex-shrink:0;}}
.h1{{font-family:'Source Serif 4',serif!important;font-weight:700;
  font-size:clamp(36px,5vw,62px);line-height:1.05;margin:0 0 6px;
  letter-spacing:-.01em;color:{INK}!important;}}

/* ══ ACRONYM LETTERS — bold red, no box, matching HTML reference ══ */
.acl{{
  color:{AC}!important;
  font-weight:700!important;
  font-family:'Source Serif 4',serif!important;
  background:none!important;
  background-color:transparent!important;
  border:none!important;
  display:inline!important;
  padding:0!important;
  margin:0!important;
  text-decoration:none!important;
  box-shadow:none!important;
  -webkit-text-fill-color:{AC}!important;
}}

.exp{{font-family:'Source Serif 4',serif!important;font-size:clamp(17px,2vw,25px);
  font-weight:400;color:{IS}!important;line-height:1.5;margin-bottom:8px;}}
.sub{{font-family:'Source Serif 4',serif!important;
  font-size:clamp(15px,2vw,20px);color:{IS}!important;
  font-style:italic;margin:6px 0 24px;}}

/* ══ CTA BUTTONS ══ */
.cta-row{{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;}}
.btn-primary{{
  font-family:'IBM Plex Sans',sans-serif!important;font-weight:600;font-size:14px;
  padding:12px 22px;
  border:1.5px solid {AC}!important;
  border-radius:2px;
  background:{AC}!important;
  color:{P}!important;
  cursor:pointer;
  text-decoration:none!important;
  display:inline-block;
  box-sizing:border-box;
  -webkit-text-fill-color:{P}!important;
}}
.btn-primary:hover{{background:{INK}!important;border-color:{INK}!important;}}
.btn-secondary{{
  font-family:'IBM Plex Sans',sans-serif!important;font-weight:600;font-size:14px;
  padding:12px 22px;
  border:1.5px solid {INK}!important;
  border-radius:2px;
  background:transparent!important;
  color:{INK}!important;
  cursor:pointer;
  text-decoration:none!important;
  display:inline-block;
  box-sizing:border-box;
  -webkit-text-fill-color:{INK}!important;
}}
.btn-secondary:hover{{background:{INK}!important;color:{P}!important;-webkit-text-fill-color:{P}!important;}}

/* Kill underlines on anchors BUT not on .btn-primary/.btn-secondary which set their own border */
div[data-testid="stMarkdownContainer"] a:not(.btn-primary):not(.btn-secondary)
{{text-decoration:none!important;border-bottom:none!important;box-shadow:none!important;}}

/* ══ SECTIONS ══ */
.sec{{padding:56px 90px;border-top:1px solid {RL};background:{P};width:100%;}}
.sec-label{{font-family:'IBM Plex Mono',monospace!important;font-size:12px;
  letter-spacing:.14em;text-transform:uppercase;color:{AC}!important;
  margin-bottom:6px;display:block;}}
.sec-label-g{{color:{GR}!important;}}
.sec-heading{{font-family:'Source Serif 4',serif!important;font-weight:600;
  font-size:clamp(22px,3vw,34px);margin:0 0 12px;color:{INK}!important;}}
.sec-intro{{font-size:15.5px;color:{IS}!important;line-height:1.75;
  max-width:700px;margin-bottom:22px;}}

/* ══ OBJECTIVE CARDS ══ */
.obj-card{{background:{CA};border:1px solid {RL};border-left:3px solid {AC};
  padding:26px 22px;min-height:130px;box-sizing:border-box;}}
.obj-num{{font-family:'IBM Plex Mono',monospace!important;font-size:26px;color:{RL}!important;
  font-weight:600;line-height:1;margin-bottom:12px;}}
.obj-text{{font-size:15px;color:{IS}!important;line-height:1.75;}}


/* ══ PHASE CARDS — CSS grid, equal height ══ */
.phase-row{{display:grid;grid-template-columns:1fr 1fr;gap:20px;}}
.phase-card{{background:{CA};border:1px solid {INK};padding:28px 24px;
  border-left:4px solid {AC};box-sizing:border-box;}}
.phase-card-2{{border-left-color:{GR};}}
.phase-tag{{font-family:'IBM Plex Mono',monospace!important;font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:{AC}!important;font-weight:600;margin-bottom:8px;}}
.phase-tag-2{{color:{GR}!important;}}
.phase-name{{font-family:'Source Serif 4',serif!important;font-size:21px;
  font-weight:600;margin-bottom:10px;color:{INK}!important;}}
.phase-desc{{font-size:14.5px;color:{IS}!important;line-height:1.75;}}

/* ══ SUB LABELS ══ */
.sub-label{{font-family:'IBM Plex Mono',monospace!important;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:{AC}!important;
  margin-bottom:10px;display:block;}}
.sub-label-g{{color:{GR}!important;}}

/* ══ METRIC CELLS ══ */
.metric-cell{{background:{P};padding:18px 12px;text-align:center;border:1px solid {RL};box-sizing:border-box;}}
.metric-num{{font-family:'IBM Plex Mono',monospace!important;font-size:clamp(18px,2.2vw,26px);
  font-weight:600;color:{AC}!important;display:block;margin-bottom:4px;}}
.metric-num-g{{color:{GR}!important;}}
.metric-lbl{{font-size:11.5px;color:{IS}!important;}}
.metric-sub{{font-family:'IBM Plex Mono',monospace!important;font-size:9.5px;color:{RU}!important;margin-top:2px;}}

/* ══ ERA SCRUBBER ══ */
.era-strip{{display:grid;grid-template-columns:repeat(4,1fr);
  border:1px solid {INK};margin-bottom:16px;overflow:hidden;border-radius:2px;}}
.era-btn{{font-family:'IBM Plex Mono',monospace!important;font-size:12px;padding:14px 6px;
  text-align:center;background:{PD};border:none;border-right:1px solid {INK};
  cursor:pointer;color:{IS}!important;transition:background 0.15s;}}
.era-btn:last-child{{border-right:none;}}
.era-btn .yr{{display:block;font-size:16px;font-weight:600;color:{INK}!important;margin-bottom:2px;}}
.era-btn .lbl{{font-size:9px;text-transform:uppercase;letter-spacing:.06em;color:{IS}!important;}}
.era-btn.active{{background:{AC}!important;}}
.era-btn.active .yr{{color:{P}!important;}}
.era-btn.active .lbl{{color:{P}!important;}}

/* ══ STEP CARDS — CSS grid, equal height ══ */
.step-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid {INK};}}
.step-card{{background:{P};padding:24px 18px;border-right:1px solid {RL};box-sizing:border-box;}}
.step-card:last-child{{border-right:none;}}
.step-num{{font-family:'IBM Plex Mono',monospace!important;font-size:26px;color:{RL}!important;
  font-weight:600;line-height:1;margin-bottom:10px;}}
.step-title{{font-family:'Source Serif 4',serif!important;font-size:16px;
  font-weight:600;margin-bottom:8px;color:{INK}!important;}}
.step-desc{{font-size:13px;color:{IS}!important;line-height:1.7;}}
.step-tag{{display:inline-block;font-family:'IBM Plex Mono',monospace!important;font-size:10px;
  color:{GR}!important;border:1px solid {GR};padding:2px 6px;margin-top:10px;
  text-transform:uppercase;letter-spacing:.04em;}}

/* ══ DELIVERABLE CARDS ══ */
.del-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid {RL};}}
.del-card{{background:{CA};padding:24px 20px;border-right:1px solid {RL};box-sizing:border-box;}}
.del-card:last-child{{border-right:none;}}
.del-num{{font-family:'IBM Plex Mono',monospace!important;font-size:24px;color:{RL}!important;
  font-weight:600;line-height:1;margin-bottom:10px;}}
.del-title{{font-family:'Source Serif 4',serif!important;font-size:16px;
  font-weight:600;margin-bottom:8px;color:{INK}!important;}}
.del-desc{{font-size:14px;color:{IS}!important;line-height:1.7;}}

/* ══ PI CARDS ══ */
.pi-card{{background:{CA};border:1px solid {RL};padding:20px 18px;margin-top:0;}}
.pi-name{{font-family:'Source Serif 4',serif!important;font-size:17px;
  font-weight:600;margin-bottom:4px;line-height:1.3;color:{INK}!important;}}
.pi-role{{font-family:'IBM Plex Mono',monospace!important;font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;color:{AC}!important;margin-bottom:6px;font-weight:600;}}
.pi-inst{{font-size:13px;color:{IS}!important;line-height:1.55;font-style:italic;}}

/* ══ METHOD TABLE ══ */
.method-table{{width:100%;border-collapse:collapse;font-family:'IBM Plex Mono',monospace!important;font-size:12px;}}
.method-table tr{{border-bottom:1px solid {RL};}}
.method-table tr:last-child{{border-bottom:none;}}
.method-table td{{padding:9px 10px;color:{IS}!important;font-size:11px;}}
.tag-rule{{display:inline-block;background:{P}!important;color:{GR}!important;border:1px solid {GR};
  padding:1px 6px;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;
  font-weight:600;border-radius:1px;}}
.tag-llm{{display:inline-block;background:{P}!important;color:{AC}!important;border:1px solid {AC};
  padding:1px 6px;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;
  font-weight:600;border-radius:1px;}}

/* ══ SPARQL QUERY CARDS ══ */
.q-card{{padding:14px 16px;border:1px solid {RL};margin-bottom:8px;background:{P};}}
.q-num{{font-size:9px;color:{AC}!important;font-weight:600;text-transform:uppercase;
  letter-spacing:.08em;display:block;margin-bottom:4px;font-family:'IBM Plex Mono',monospace!important;}}
.q-title{{color:{INK}!important;font-size:12px;font-weight:600;display:block;
  margin-bottom:6px;font-family:'IBM Plex Mono',monospace!important;}}
.q-desc{{font-size:11px;color:{IS}!important;font-family:'IBM Plex Mono',monospace!important;}}

/* ══ OWL / DARK CODE BLOCKS
   · background forced ink
   · ALL text children forced to cream via !important on every selector
   · ::selection override so browser highlight doesn't show blue
   · user-select:text kept but selection colour overridden
══ */
.dark-block{{
  background:{INK}!important;
  padding:20px 22px;
  border-radius:2px;
  overflow:auto;
}}
.dark-block *{{
  background:transparent!important;
  color:{CA}!important;
  font-family:'IBM Plex Mono',monospace!important;
}}
.dark-block pre{{
  margin:0;
  font-size:11.5px;
  line-height:1.8;
  white-space:pre-wrap;
  color:{CA}!important;
}}
.dark-block ::selection{{background:{AC};color:{P};}}
.dark-block ::-moz-selection{{background:{AC};color:{P};}}
/* Named spans inside dark blocks — use data-attrs via inline style only, CSS here as fallback */
.dark-block .hl-orange{{color:{ACS}!important;font-weight:600;}}
.dark-block .hl-rule{{color:{RL}!important;}}
.dark-block .hl-cream{{color:{CA}!important;}}

/* ══ CONTACT ══ */
.contact-block{{border:1px solid {RL};background:{CA};padding:26px;
  display:flex;align-items:center;gap:20px;margin-top:20px;}}
.contact-dot{{width:8px;height:8px;border-radius:50%;background:{AC};flex-shrink:0;}}
.contact-label{{font-family:'IBM Plex Mono',monospace!important;font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:{RU}!important;display:block;margin-bottom:4px;font-weight:600;}}
.contact-email{{font-family:'IBM Plex Mono',monospace!important;font-size:16px;
  font-weight:600;color:{GR}!important;text-decoration:none!important;}}

/* ══ FOOTER ══ */
.footer{{border-top:3px solid {INK};padding:24px 90px 32px;
  font-family:'IBM Plex Mono',monospace!important;font-size:12px;color:{IS}!important;background:{P};}}

/* ══════════════════════════════════════════════════
   STREAMLIT COMPONENT OVERRIDES
   ══════════════════════════════════════════════════ */

/* TABS */
.stTabs [data-baseweb="tab-list"]
{{background:{PD}!important;border-bottom:2px solid {INK}!important;
  gap:0!important;padding:0!important;margin:0!important;}}
.stTabs [data-baseweb="tab"]
{{font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;
  color:{IS}!important;background:{PD}!important;
  border-radius:0!important;padding:13px 26px!important;
  border-right:1px solid {RL}!important;border-bottom:none!important;}}
.stTabs [aria-selected="true"]
{{background:{CA}!important;color:{INK}!important;
  border-top:2px solid {AC}!important;font-weight:600!important;}}
.stTabs [data-baseweb="tab-panel"]
{{background:{P}!important;padding:0!important;}}

/* ALL Streamlit buttons */
button[kind="primary"],button[kind="secondary"],
.stButton>button,.stFormSubmitButton>button
{{font-family:'IBM Plex Mono',monospace!important;font-size:12px!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;
  background:{AC}!important;color:{P}!important;
  border:1.5px solid {AC}!important;border-radius:2px!important;
  padding:10px 20px!important;font-weight:600!important;
  min-width:160px!important;}}
.stButton>button:hover,.stFormSubmitButton>button:hover
{{background:{INK}!important;border-color:{INK}!important;}}

/* Download buttons */
.stDownloadButton>button
{{background:{P}!important;color:{INK}!important;
  border:1.5px solid {INK}!important;min-width:160px!important;}}
.stDownloadButton>button:hover
{{background:{INK}!important;color:{P}!important;}}

/* FILE UPLOADER */
[data-testid="stFileUploader"],
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] > div > div,
[data-testid="stFileUploaderDropzone"] label
{{background:{CA}!important;color:{IS}!important;}}
[data-testid="stFileUploaderDropzone"]
{{border:1.5px dashed {RL}!important;border-radius:2px!important;padding:20px!important;}}
[data-testid="stFileUploaderDropzone"] *
{{color:{IS}!important;background:{CA}!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:12px!important;}}
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-secondary"]
{{background:{AC}!important;color:{P}!important;
  border:1px solid {AC}!important;border-radius:2px!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;
  padding:8px 16px!important;min-width:unset!important;}}
[data-testid="stFileUploaderDropzone"] svg
{{fill:{RU}!important;stroke:{RU}!important;}}

/* SELECT / DROPDOWN */
[data-baseweb="select"]>div,
[data-baseweb="select"] *,
[data-baseweb="select"] [data-baseweb="input"],
[data-baseweb="select"] [data-baseweb="input"] *
{{background:{CA}!important;color:{INK}!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:12px!important;
  border-color:{RL}!important;}}
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="popover"] *,
[data-baseweb="menu"] *
{{background:{CA}!important;color:{INK}!important;
  font-family:'IBM Plex Mono',monospace!important;}}
[data-baseweb="menu"] [role="option"]
{{background:{CA}!important;color:{INK}!important;}}
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"]
{{background:{PD}!important;color:{INK}!important;}}

/* TEXT AREA */
.stTextArea textarea
{{background:{CA}!important;border:1px solid {RL}!important;
  border-radius:2px!important;font-family:'IBM Plex Mono',monospace!important;
  font-size:12px!important;color:{INK}!important;}}

/* PROGRESS BAR */
.stProgress > div > div > div > div{{background:{AC}!important;}}
[data-testid="stProgressBar"] > div{{background:{AC}!important;}}
.stProgress [role="progressbar"]{{background:{RL}!important;border-radius:2px!important;}}
.stProgress [role="progressbar"] > div{{background:{AC}!important;border-radius:2px!important;}}

/* ALERTS */
[data-testid="stAlert"]
{{background:{CA}!important;border-left:4px solid {AC}!important;border-radius:2px!important;}}
[data-testid="stAlert"] p,[data-testid="stAlert"] span{{color:{INK}!important;}}
[data-testid="stSuccessAlert"]{{border-left-color:{GR}!important;}}
[data-testid="stWarningAlert"]{{border-left-color:{ACS}!important;}}
[data-testid="stInfoAlert"]{{border-left-color:{RU}!important;}}

/* CHECKBOX */
.stCheckbox span
{{font-family:'IBM Plex Sans',sans-serif!important;font-size:14px!important;color:{INK}!important;}}

/* SLIDER */
[data-baseweb="slider"] [role="slider"]{{background:{AC}!important;border-color:{AC}!important;}}

/* SPINNER */
[data-testid="stSpinner"] svg *{{stroke:{AC}!important;}}

/* IMAGE */
[data-testid="stImage"]{{margin:0!important;}}
[data-testid="stImage"] img{{display:block;width:100%;border:1.5px solid {INK};}}

hr{{border:none;border-top:1px solid {RL};margin:28px 0;}}
@media(prefers-reduced-motion:reduce){{*{{transition:none!important;}}}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────
def render_html_table(df_or_rows, columns=None):
    if isinstance(df_or_rows, pd.DataFrame):
        cols = list(df_or_rows.columns) if columns is None else columns
        rows = df_or_rows.values.tolist()
    else:
        cols = list(df_or_rows[0].keys()) if columns is None else columns
        rows = [[r.get(c, "") for c in cols] for r in df_or_rows]
    th = "".join(
        f'<th style="padding:9px 12px;text-align:left;background:{PD};'
        f'font-family:IBM Plex Mono,monospace;font-size:11px;color:{IS};'
        f'letter-spacing:.08em;text-transform:uppercase;'
        f'border-bottom:2px solid {INK};border-right:1px solid {RL};">{c}</th>'
        for c in cols)
    tbody = "".join(
        "<tr>" + "".join(
            f'<td style="padding:8px 12px;border-bottom:1px solid {RL};'
            f'border-right:1px solid {RL};font-family:IBM Plex Mono,monospace;'
            f'font-size:12px;color:{INK};background:{CA};">{v}</td>'
            for v in row) + "</tr>"
        for row in rows)
    return (f'<div style="overflow-x:auto;">'
            f'<table style="width:100%;border-collapse:collapse;background:{CA};border:1px solid {RL};">'
            f'<thead><tr>{th}</tr></thead><tbody>{tbody}</tbody></table></div>')

def dark_code(content_html, extra_style=""):
    """Wrap pre-formatted content in a dark ink block with full inline style redundancy."""
    return (f'<div style="background:{INK};padding:24px 28px;border-radius:2px;'
            f'overflow:auto;{extra_style}">'
            f'<pre style="margin:0;font-family:IBM Plex Mono,monospace;font-size:12.5px;'
            f'line-height:1.9;white-space:pre-wrap;color:{CA};background:transparent;">'
            f'{content_html}</pre></div>')

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def resolve_path(path):
    return path if os.path.isabs(path) else os.path.join(APP_DIR, path)

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def show_img(path, height=280, fit="cover", object_position="center top"):
    full_path = resolve_path(path)
    if os.path.exists(full_path):
        ext = os.path.splitext(full_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        b64 = img_to_base64(full_path)
        st.markdown(
            f'<img src="data:image/{mime};base64,{b64}" '
            f'style="width:100%;height:{height}px;object-fit:{fit};'
            f'object-position:{object_position};display:block;'
            f'border:1.5px solid {INK};box-sizing:border-box;">',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="background:{PD};border:1.5px solid {RL};height:{height}px;'
            f'display:flex;align-items:center;justify-content:center;'
            f'color:{RU};font-family:IBM Plex Mono,monospace;font-size:11px;">'
            f'{os.path.basename(path)}</div>', unsafe_allow_html=True)

# ── Backend ────────────────────────────────────────────────────────────────
MISTRAL_API_KEY = st.secrets.get("MISTRAL_API_KEY", "")
DEFAULT_JSON_PATH = os.path.join(APP_DIR, 'matrimonial_ads_cleaned.json')
ONTOLOGY_IRI      = "http://matrimonial-nlp-research.org/ontology#"

SPARQL_PREFIX = f"""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mat: <{ONTOLOGY_IRI}>
"""
SPARQL_QUERIES = {
    "① All Grooms — age, caste, education": SPARQL_PREFIX + """
SELECT ?groom ?age ?caste ?education
WHERE {
    ?groom rdf:type mat:Groom .
    OPTIONAL { ?groom mat:hasAge            ?age       }
    OPTIONAL { ?groom mat:hasCasteName      ?caste     }
    OPTIONAL { ?groom mat:hasEducationLevel ?education }
} ORDER BY ?age""",
    "② Age distribution": SPARQL_PREFIX + """
SELECT ?age (COUNT(?person) AS ?count)
WHERE { ?person mat:hasAge ?age . }
GROUP BY ?age ORDER BY ASC(?age)""",
    "③ Grooms aged 30+": SPARQL_PREFIX + """
SELECT ?groom ?age ?education ?profession
WHERE {
    ?groom rdf:type mat:Groom .
    ?groom mat:hasAge ?age . FILTER (?age >= 30)
    OPTIONAL { ?groom mat:hasEducationLevel ?education }
    OPTIONAL { ?groom mat:hasProfession     ?profession }
} ORDER BY DESC(?age)""",
    "④ Caste-no-bar preferences": SPARQL_PREFIX + """
SELECT ?groom ?age ?caste ?castePref
WHERE {
    ?groom rdf:type mat:Groom .
    ?groom mat:hasRequirement ?req .
    ?req   mat:preferredCaste ?castePref .
    FILTER (REGEX(?castePref,"no bar","i"))
    OPTIONAL { ?groom mat:hasAge       ?age   }
    OPTIONAL { ?groom mat:hasCasteName ?caste }
}""",
    "⑤ Brahmin grooms — height & box": SPARQL_PREFIX + """
SELECT ?groom ?age ?height ?box
WHERE {
    ?groom rdf:type mat:Groom .
    ?groom mat:hasCasteName ?caste .
    FILTER (REGEX(?caste,"Brahmin","i"))
    OPTIONAL { ?groom mat:hasAge    ?age    }
    OPTIONAL { ?groom mat:hasHeight ?height }
    ?ad    mat:advertises ?groom .
    OPTIONAL { ?ad    mat:hasBoxNumber ?box }
}""",
    "⑥ Custom query": SPARQL_PREFIX + """
SELECT ?subject ?predicate ?object
WHERE { ?subject ?predicate ?object . } LIMIT 30""",
}

class MatrimonialExtractor:
    def __init__(self):
        self.caste_dict = {
            'Brahmin':   ['ব্রাহ্মণ','brahmin','brahman'],
            'Kayastha':  ['কায়স্থ','kayastha'],
            'Baidya':    ['বৈদ্য','baidya','vaidya'],
            'Banerjee':  ['banerjee','bandyopadhyay'],
            'Mukherjee': ['mukherjee','mukhopadhyay'],
            'Chatterjee':['chatterjee','chattopadhyay'],
        }
    def _norm(self,t):
        for b,e in zip('০১২৩৪৫৬৭৮৯','0123456789'): t=t.replace(b,e)
        return t
    def detect_roles(self,text):
        for p in ['পাত্রী চাই','bride wanted']:
            if p in text: return {'advertiser_role':'groom','seeking':'bride'}
        for p in ['পাত্র চাই','groom wanted']:
            if p in text: return {'advertiser_role':'bride','seeking':'groom'}
        return {'advertiser_role':'groom','seeking':'bride'}
    def extract_age(self,text):
        t=self._norm(text)
        m=re.search(r'\b(\d{2})\s*[/]\s*\d+[\'\'-]',t)
        if m: return int(m.group(1))
        for c in re.findall(r'\b([1-5][0-9])\b(?!\d)',t):
            v=int(c)
            if 18<=v<=60: return v
        return None
    def extract_height(self,text):
        t=self._norm(text); sep=r"[\''′`´\-–—\s]"
        m=re.search(rf'\b(\d){sep}{{1,4}}(\d{{1,2}})\b',t)
        if m:
            f,i=int(m.group(1)),int(m.group(2))
            if 4<=f<=7 and 0<=i<=11: return f"{f}'{i}\""
        return None
    def extract_caste(self,text):
        tl=text.lower()
        for name,variants in self.caste_dict.items():
            for v in variants:
                if v.lower() in tl: return name
        return None
    def extract_box(self,text):
        m=re.search(r'(?:box|বক্স)[\s:।]*(\d{3,5})',text,re.IGNORECASE)
        return m.group(1) if m else None
    def extract_pref_age(self,text):
        t=self._norm(text); amin,amax=None,None
        m=re.search(r'(?:upto|up to|below|under)\s*(\d{2})',t,re.IGNORECASE)
        if m: amax=int(m.group(1))
        m=re.search(r'(\d{2})\s*(?:to|-)\s*(\d{2})\s*(?:years?|yrs?)?',t,re.IGNORECASE)
        if m: amin,amax=int(m.group(1)),int(m.group(2))
        return amin,amax
    def extract_caste_pref(self,text):
        tl=text.lower()
        if re.search(r'caste\s*no\s*bar|no\s*bar',tl): return 'no bar'
        for name,variants in self.caste_dict.items():
            for v in variants:
                if v.lower() in tl: return name
        return None
    def extract_all(self,text):
        roles=self.detect_roles(text); amin,amax=self.extract_pref_age(text)
        return {
            'advertiser':{'role':roles['advertiser_role'],'age':self.extract_age(text),
                          'height':self.extract_height(text),'caste':self.extract_caste(text),
                          'education':None,'profession':None},
            'requirements':{'seeking':roles['seeking'],'caste_preference':self.extract_caste_pref(text),
                            'age_min':amin,'age_max':amax,'other_preferences':None},
            'contact':{'box_number':self.extract_box(text)},
        }

class MistralExtractor:
    def __init__(self):
        import requests; self.req=requests
        self.url="https://api.mistral.ai/v1/chat/completions"
        self.model="mistral-small-latest"
        self.hdr={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}
    def extract(self,text):
        prompt=(f'Extract from this matrimonial ad.\n{text}\n'
                f'Return ONLY JSON: {{"education":"...or null","profession":"...or null","other_preferences":"...or null"}}')
        try:
            r=self.req.post(self.url,headers=self.hdr,
              json={"model":self.model,"messages":[{"role":"user","content":prompt}],
                    "temperature":0.1,"max_tokens":200,"response_format":{"type":"json_object"}},timeout=30)
            if r.status_code==200: return json.loads(r.json()['choices'][0]['message']['content'])
        except: pass
        return {'education':None,'profession':None,'other_preferences':None}

class HybridExtractor:
    def __init__(self,use_llm=True):
        self.rule=MatrimonialExtractor()
        self.llm=MistralExtractor() if use_llm else None
    def extract(self,text,use_llm=True):
        r=self.rule.extract_all(text)
        if use_llm and self.llm:
            lr=self.llm.extract(text)
            r['advertiser']['education']=lr.get('education')
            r['advertiser']['profession']=lr.get('profession')
            r['requirements']['other_preferences']=lr.get('other_preferences')
        return r

def build_ontology(extractions):
    from owlready2 import get_ontology,Thing,ObjectProperty,DataProperty,FunctionalProperty
    try:
        from owlready2 import default_world; default_world.ontologies.clear()
    except: pass
    onto=get_ontology(ONTOLOGY_IRI)
    with onto:
        class Person(Thing): pass
        class Groom(Person): pass
        class Bride(Person): pass
        class Advertisement(Thing): pass
        class Requirement(Thing): pass
        class advertises(ObjectProperty): domain=[Advertisement]; range=[Person]
        class seeks(ObjectProperty): domain=[Person]; range=[Person]
        class hasRequirement(ObjectProperty): domain=[Person]; range=[Requirement]
        class hasAge(DataProperty,FunctionalProperty): domain=[Person]; range=[int]
        class hasHeight(DataProperty,FunctionalProperty): domain=[Person]; range=[str]
        class hasCasteName(DataProperty,FunctionalProperty): domain=[Person]; range=[str]
        class hasEducationLevel(DataProperty,FunctionalProperty): domain=[Person]; range=[str]
        class hasProfession(DataProperty,FunctionalProperty): domain=[Person]; range=[str]
        class hasBoxNumber(DataProperty,FunctionalProperty): domain=[Advertisement]; range=[str]
        class preferredAgeMin(DataProperty,FunctionalProperty): domain=[Requirement]; range=[int]
        class preferredAgeMax(DataProperty,FunctionalProperty): domain=[Requirement]; range=[int]
        class preferredCaste(DataProperty,FunctionalProperty): domain=[Requirement]; range=[str]
        for i,ext in enumerate(extractions):
            adv=ext.get('advertiser',{}); role=adv.get('role','groom')
            p=Groom(f"groom_{i+1}") if role=='groom' else Bride(f"bride_{i+1}")
            if adv.get('age'): p.hasAge=int(adv['age'])
            if adv.get('height'): p.hasHeight=str(adv['height'])
            if adv.get('caste'): p.hasCasteName=str(adv['caste'])
            if adv.get('education'): p.hasEducationLevel=str(adv['education'])
            if adv.get('profession'): p.hasProfession=str(adv['profession'])
            ad=Advertisement(f"ad_{i+1}"); ad.advertises=[p]
            box=ext.get('contact',{}).get('box_number')
            if box: ad.hasBoxNumber=str(box)
            rd=ext.get('requirements',{}); req=Requirement(f"req_{i+1}"); p.hasRequirement=[req]
            if rd.get('age_min'): req.preferredAgeMin=int(rd['age_min'])
            if rd.get('age_max'): req.preferredAgeMax=int(rd['age_max'])
            if rd.get('caste_preference'): req.preferredCaste=str(rd['caste_preference'])
    path=os.path.join(tempfile.gettempdir(),"matrimonial.owl")
    onto.save(file=path,format="rdfxml"); return path

def run_sparql(owl_path,query):
    from rdflib import Graph as RG
    g=RG(); g.parse(owl_path,format='xml')
    try:
        res=g.query(query)
        rows=[[str(x) for x in row] for row in res]
        if rows:
            df=pd.DataFrame(rows,columns=[str(v) for v in res.vars])
            for col in df.columns:
                df[col]=df[col].apply(lambda v: v.split('#')[-1] if '#' in v else v)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Query error: {e}"); return pd.DataFrame()

def kg_pyvis(extractions):
    try: from pyvis.network import Network
    except ImportError: return None
    net=Network(height="520px",width="100%",bgcolor=CA,font_color=INK,directed=True)
    net.barnes_hut(gravity=-8000,central_gravity=0.3,spring_length=120)
    schema={"Advertisement":(AC,"square"),"Person":(RU,"square"),
            "Groom":(ACS,"square"),"Bride":(GR,"square"),"Requirement":(IS,"dot")}
    for name,(color,shape) in schema.items():
        net.add_node(name,label=name,color=color,shape=shape,size=28,
                     font={"size":13,"face":"monospace","color":INK,"bold":True},borderWidth=2)
    net.add_edge("Advertisement","Person",label="advertises",color=AC,width=2)
    net.add_edge("Groom","Person",label="subClassOf",color=RL,width=1,dashes=True)
    net.add_edge("Bride","Person",label="subClassOf",color=RL,width=1,dashes=True)
    net.add_edge("Person","Requirement",label="hasRequirement",color=GR,width=2)
    for i,ext in enumerate(extractions[:25]):
        adv=ext.get('advertiser',{}); role=adv.get('role','groom')
        age=adv.get('age','?'); caste=adv.get('caste',''); edu=adv.get('education','')
        aid=f"ad_{i+1}"; pid=f"{'groom' if role=='groom' else 'bride'}_{i+1}"; rid=f"req_{i+1}"
        box=ext.get('contact',{}).get('box_number')
        net.add_node(aid,label=f"Ad #{i+1}"+(f"\nBox {box}" if box else ""),
                     color=CA,shape="square",size=16,font={"size":9,"face":"monospace","color":INK},borderWidth=1)
        pl=f"{'♂' if role=='groom' else '♀'} {age}"
        if caste: pl+=f"\n{caste}"
        if edu:   pl+=f"\n{edu}"
        net.add_node(pid,label=pl,color={"background":P if role=='groom' else PD,
                     "border":AC if role=='groom' else GR},shape="square",size=20,
                     font={"size":9,"face":"monospace","color":INK},borderWidth=2)
        rd=ext.get('requirements',{}); rp=[]
        if rd.get('caste_preference'): rp.append(rd['caste_preference'])
        if rd.get('age_max'):          rp.append(f"≤{rd['age_max']}yr")
        net.add_node(rid,label="\n".join(rp) if rp else "req",
                     color={"background":PD,"border":GR},shape="dot",size=12,
                     font={"size":8,"face":"monospace","color":GR},borderWidth=1)
        net.add_edge(aid,pid,label="advertises",color=AC,width=1)
        net.add_edge(pid,rid,label="hasReq",color=GR,width=1)
        net.add_edge(pid,"Groom" if role=='groom' else "Bride",label="type",color=RL,width=1,dashes=True)
    net.set_options('{"edges":{"arrows":{"to":{"enabled":true,"scaleFactor":0.6}},'
                    '"font":{"size":8,"face":"monospace"}},'
                    '"physics":{"barnesHut":{"gravitationalConstant":-8000}}}')
    hp=os.path.join(tempfile.gettempdir(),"kg.html"); net.save_graph(hp)
    with open(hp,"r",encoding="utf-8") as f: html=f.read()
    html=html.replace("body {",f"body {{ background:{CA} !important; margin:0; padding:0; ")
    return html

def ontology_fig(extractions):
    import networkx as nx
    G=nx.DiGraph()
    classes=["Thing","Advertisement","Person","Groom","Bride","Requirement"]
    dprops=["hasAge","hasHeight","hasCasteName","hasEducationLevel",
            "hasProfession","hasBoxNumber","preferredAgeMin","preferredAgeMax","preferredCaste"]
    for n in classes: G.add_node(n,ntype="c")
    for p in dprops:  G.add_node(p,ntype="d")
    for s,t,l in [("Thing","Advertisement",""),("Thing","Person",""),("Thing","Requirement",""),
                  ("Person","Groom","subClassOf"),("Person","Bride","subClassOf")]:
        G.add_edge(s,t,label=l,etype="sub")
    for s,t,l in [("Advertisement","Person","advertises"),("Person","Requirement","hasRequirement")]:
        G.add_edge(s,t,label=l,etype="obj")
    dp_map={"Advertisement":["hasBoxNumber"],"Person":["hasAge","hasHeight","hasCasteName","hasEducationLevel","hasProfession"],
            "Requirement":["preferredAgeMin","preferredAgeMax","preferredCaste"]}
    for cls,props in dp_map.items():
        for p in props: G.add_edge(cls,p,label="",etype="data")
    pos={"Thing":(0,0),"Advertisement":(-3.5,-2),"Person":(0,-2),"Requirement":(3.5,-2),
         "Groom":(-1.5,-4),"Bride":(1.5,-4),"hasBoxNumber":(-6,-2),
         "hasAge":(-2.5,-5.5),"hasHeight":(-0.8,-5.5),"hasCasteName":(0.8,-5.5),
         "hasEducationLevel":(2.5,-5.5),"hasProfession":(4.5,-5.5),
         "preferredAgeMin":(5,-2),"preferredAgeMax":(6.5,-2),"preferredCaste":(8,-2)}
    fig,ax=plt.subplots(figsize=(18,11))
    fig.patch.set_facecolor(CA); ax.set_facecolor(P)
    for node in classes:
        x,y=pos[node]
        ax.add_patch(mpatches.FancyBboxPatch((x-.7,y-.27),1.4,.54,
            boxstyle="round,pad=0.08",edgecolor=AC,facecolor=CA,linewidth=2.5,zorder=2))
        ax.text(x,y,node,fontsize=11,fontweight='bold',ha='center',va='center',
                color=INK,family='monospace',zorder=3)
    for node in dprops:
        x,y=pos[node]
        ax.add_patch(mpatches.FancyBboxPatch((x-.65,y-.2),1.3,.4,
            boxstyle="round,pad=0.05",edgecolor=GR,facecolor=PD,linewidth=1.8,zorder=2))
        ax.text(x,y,node,fontsize=8,ha='center',va='center',
                color=GR,family='monospace',zorder=3,style='italic')
    sub_e=[(s,t) for s,t,d in G.edges(data=True) if d.get('etype')=='sub']
    obj_e=[(s,t) for s,t,d in G.edges(data=True) if d.get('etype')=='obj']
    dat_e=[(s,t) for s,t,d in G.edges(data=True) if d.get('etype')=='data']
    nx.draw_networkx_edges(G,pos,edgelist=sub_e,edge_color=ACS,style='dashed',
        arrows=True,arrowsize=18,width=1.8,ax=ax,connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G,pos,edgelist=obj_e,edge_color=AC,style='solid',
        arrows=True,arrowsize=22,width=2.5,ax=ax,connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G,pos,edgelist=dat_e,edge_color=GR,style='dotted',
        arrows=True,arrowsize=12,width=1.5,ax=ax)
    for (s,t),label in {(s,t):d['label'] for s,t,d in G.edges(data=True) if d.get('label')}.items():
        x=(pos[s][0]+pos[t][0])/2; y=(pos[s][1]+pos[t][1])/2
        ax.text(x,y,label,fontsize=7,ha='center',va='center',color=IS,family='monospace',
                bbox=dict(boxstyle='round,pad=0.25',facecolor=CA,edgecolor=RL,linewidth=1),zorder=4)
    ax.legend(handles=[
        mpatches.Patch(facecolor=CA,edgecolor=AC,linewidth=2.5,label="OWL Class"),
        mpatches.Patch(facecolor=PD,edgecolor=GR,linewidth=1.8,label="Data Property"),
        mpatches.Patch(color=AC,label="Object Property",linewidth=2.5),
        mpatches.Patch(color=ACS,label="subClassOf",linewidth=1.8,linestyle='--')],
        loc="upper right",framealpha=0.95,labelcolor=INK,facecolor=CA,edgecolor=RL,fontsize=9,
        prop={"family":"monospace"},title="Legend",
        title_fontproperties={"family":"serif","size":10,"weight":"bold"})
    ax.set_title("OWL Ontology — Class Hierarchy & Property Relationships",
                 fontsize=13,color=INK,fontfamily="serif",fontweight='bold',pad=16,
                 bbox=dict(boxstyle='round,pad=0.6',facecolor=CA,edgecolor=RL,linewidth=2))
    ax.axis("off"); plt.tight_layout(); return fig

# ── Session state ──────────────────────────────────────────────────────────
for k,v in [('extractions',[]),('owl_path',None),('raw_ads',[]),
             ('loaded',False),('last_df',None),('era','1984')]:
    if k not in st.session_state: st.session_state[k]=v

ERA = {
    "1984":{"imgs":["images/newspapers/1984_1.png","images/newspapers/1984_2.png"],
            "cap":f"<b>1984 — Dense-packing era.</b> Hand-set hot-metal columns, hairline rules, near-zero whitespace between listings. Ink-bleed and paper aging are common.","lbl":"Dense-packing"},
    "1998":{"imgs":["images/newspapers/1998_1.png","images/newspapers/1998_2.png"],
            "cap":f"<b>1998 — Early phototypesetting.</b> Column counts increase as desktop publishing tools enter newsrooms.","lbl":"Phototypeset"},
    "2010":{"imgs":["images/newspapers/2010_1.png","images/newspapers/2010_2.png"],
            "cap":f"<b>2010 — Standardised grid.</b> Digital typesetting introduces consistent gutters and grid-aligned columns.","lbl":"Grid layout"},
    "2024":{"imgs":["images/newspapers/2024_1.png","images/newspapers/2024_2.png"],
            "cap":f"<b>2024 — Digital hybrid layout.</b> Rounded card-like ad blocks, variable typography, and design flourishes appear.","lbl":"Digital hybrid"},
}

qp = st.query_params
if "era" in qp: st.session_state.era = qp["era"]

# ══════════════════════════════════════════════════════════════════════════════
# MASTHEAD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="masthead">
  <div class="masthead-inner">
    <span class="mh-brand">PORINOY</span>
    <span class="mh-nav">Methodology &nbsp;·&nbsp; Team &nbsp;·&nbsp; Contact</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO — acronym letters via inline style only (no class dependence)
# ══════════════════════════════════════════════════════════════════════════════
def acl(letter):
    return (f'<span style="color:{AC};font-weight:700;font-family:\'Source Serif 4\',serif;'
            f'background:none;background-color:transparent;border:none;'
            f'display:inline;padding:0;margin:0;text-decoration:none;">{letter}</span>')

st.markdown(f"""
<div class="hero">
  <div class="wrap">
    <p class="kicker">Research Project under the Jaya Prakash Narayan National Centre of Excellence in Humanities, IIT Indore</p>
    <h1 class="h1">PORINOY</h1>
    <p class="exp">{acl("P")}roducing&nbsp;{acl("O")}ntologies of&nbsp;{acl("R")}elationships from&nbsp;{acl("I")}ndian&nbsp;{acl("N")}uptial d{acl("O")}cuments longitudinall{acl("Y")}</p>
    <p class="sub">A Case Study of Bengali / Bangla Wedding Invitations</p>
    <div class="cta-row">
      <a class="btn-primary" href="#approach" style="text-decoration:none;">Explore the Project &rarr;</a>
      <a class="btn-secondary" href="#contact" style="text-decoration:none;">Get in Touch</a>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec"><div class="wrap">', unsafe_allow_html=True)
st.markdown(f"""
<span class="sec-label">Objectives</span>
<h2 class="sec-heading">What this research sets out to do</h2>
<p class="sec-intro">Collecting, analysing, and computing over Bengali/Bangla matrimonial documents to trace socio-cultural transitions in Bengal from "tradition" to "modernity."</p>
""", unsafe_allow_html=True)

with st.container(key="obj_cards"):
    oc1, oc2 = st.columns(2, gap="large")
    with oc1:
        st.markdown(f'<div class="obj-card"><div class="obj-num">I</div><p class="obj-text">Collecting, digitising, and analysing Bengali/Bangla matrimonial documents as vehicles of socio-cultural transitions in Bengal through systematic archival and computational methods.</p></div>', unsafe_allow_html=True)
    with oc2:
        st.markdown(f'<div class="obj-card"><div class="obj-num">II</div><p class="obj-text">Examining changing discourses of Bengali weddings and marriage practices, and of the networks of relationships they have influenced and inflected, as indicators of broader societal transitions.</p></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec"><div class="wrap">', unsafe_allow_html=True)
st.markdown(f"""
<span class="sec-label">Methodology</span>
<h2 class="sec-heading">A two-phase approach</h2>
<p class="sec-intro">The project involves multidisciplinary methods to comprehensively investigate the dynamics of Bengali wedding documents.</p>
<div class="phase-row">
  <div class="phase-card">
    <p class="phase-tag">Phase I</p>
    <p class="phase-name">BANDHAN Dataset Creation</p>
    <p class="phase-desc">Intensive archival research, collection of analogue and digital documents, OCR digitisation, and creation of <strong>BANDHAN</strong> - Bengali Advertisement Newspaper Dataset for Historical Analysis of Nuptials -
    spanning four decades (1984–2024).</p>
  </div>
  <div class="phase-card phase-card-2">
    <p class="phase-tag phase-tag-2">Phase II</p>
    <p class="phase-name">Domain-Specific Analysis</p>
    <p class="phase-desc">Establishing ontologies of relationships within the Bengali wedding documents, and building a comprehensive computational view of societal transitions using NLP pipelines, OWL ontologies, and SPARQL-based semantic querying.</p>
  </div>
</div>""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROPOSED APPROACH
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div id="approach" style="padding:52px 0 0 0;background:{P};width:100%;">
  <div class="wrap">
    <span class="sec-label">Proposed Approach</span>
    <h2 class="sec-heading">An integrated knowledge portal</h2>
    <p class="sec-intro">An invaluable resource offering insights into the cultural practices and transitions in Bengali wedding and marriage practices over time.</p>
  </div>
</div>""", unsafe_allow_html=True)

tab_p1, tab_p2 = st.tabs(["Phase I — Dataset & Corpus","Phase II — NLP, Ontology & Queries"])

# ─── PHASE I ────────────────────────────────────────────────────────────────
with tab_p1:
    st.markdown('<div class="wrap" style="padding-top:32px;padding-bottom:48px;">', unsafe_allow_html=True)

# ── Era scrubber: real Streamlit buttons, so a click just reruns + updates state ──
    st.markdown(f"""
    <style>
    .st-key-era_row [data-testid="stHorizontalBlock"] {{ gap:0 !important; border:1px solid {INK}; border-radius:2px; overflow:hidden; }}
    .st-key-era_row [data-testid="stColumn"] {{ padding:0 !important; }}
    .st-key-era_row [data-testid="stColumn"]:not(:last-child) {{ border-right:1px solid {INK}; }}
    .st-key-era_row button {{
        width:100% !important; min-width:0 !important;
        border:none !important; border-radius:0 !important;
        background:{PD} !important; padding:14px 6px !important;
    }}
    .st-key-era_row button p {{
        font-family:'IBM Plex Mono',monospace !important;
        color:{IS} !important; margin:0 !important; line-height:1.4;
    }}
    .st-key-era_row button p:first-child {{ font-size:16px !important; font-weight:600 !important; color:{INK} !important; }}
    .st-key-era_row button p:last-child  {{ font-size:9px !important; text-transform:uppercase; letter-spacing:.06em; }}
    .st-key-era_row button[kind="primary"]   {{ background:{AC} !important; }}
    .st-key-era_row button[kind="primary"] p {{ color:{P} !important; }}
    .st-key-era_row button:hover {{ background:{RL} !important; }}
    </style>""", unsafe_allow_html=True)

    with st.container(key="era_row"):
        era_cols = st.columns(4, gap="small")
        for col, k in zip(era_cols, ERA):
            with col:
                if st.button(f"{k}\n\n{ERA[k]['lbl']}", key=f"era_btn_{k}",
                             type="primary" if st.session_state.era == k else "secondary",
                             use_container_width=True):
                    st.session_state.era = k
                    st.rerun()

    cur_era = ERA[st.session_state.era]
    ic1,ic2=st.columns(2,gap="small")
    with ic1: show_img(cur_era["imgs"][0], height=320, fit="contain")
    with ic2: show_img(cur_era["imgs"][1], height=320, fit="contain")
    st.markdown(f'<p style="font-size:13.5px;color:{IS};margin-top:28px;line-height:1.65;">{cur_era["cap"]}</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    cl,cr=st.columns(2,gap="large")
    with cl:
        st.markdown(f'<span class="sub-label">Sourcing & Digitisation</span>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:15px;color:{IS};line-height:1.75;">We performed <strong style="color:{INK}">stratified sampling</strong> from six major Bengali newspapers: Ananda Bazar Patrika, Bartaman, Ei Samay, Sangbad Pratidin, Aajkaal, and Ganashakti. Physical copies were digitised at <strong style="color:{INK}">300 DPI</strong> using flatbed scanners.</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:15px;color:{IS};line-height:1.75;">Sampling was designed to maximise temporal coverage across four print-technology eras, deliberately capturing systematic variation in typesetting convention and document degradation.</p>', unsafe_allow_html=True)
    with cr:
        st.markdown(f'<span class="sub-label">Dataset at a glance</span>', unsafe_allow_html=True)
        mc1,mc2=st.columns(2,gap="small"); mc3,mc4=st.columns(2,gap="small")
        for cm,num,lbl in [(mc1,"40","year archive"),(mc2,"6","newspapers"),
                            (mc3,"3","layout classes"),(mc4,"κ>0.85","inter-annotator")]:
            with cm:
                st.markdown(f'<div class="metric-cell"><span class="metric-num">{num}</span><span class="metric-lbl">{lbl}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<br><span class="sub-label">Annotation Pipeline: Human in the Loop</span>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="step-row">
  <div class="step-card">
    <div class="step-num">01</div>
    <p class="step-title">Layout Segmentation</p>
    <p class="step-desc">Spatial regions annotated across three semantic classes: <em>Advertisement</em>, <em>Bride</em>, and <em>Groom</em>. Annotators held to a strict 2px boundary tolerance.</p>
    <span class="step-tag">COCO JSON</span>
  </div>
  <div class="step-card">
    <div class="step-num">02</div>
    <p class="step-title">Multi-engine OCR Drafting</p>
    <p class="step-desc">Custom GUI <strong>3-Netra</strong> generates baseline transcriptions using three OCR engines: OLM-OCR2, DeepSeek-VL, and EasyOCR, run in parallel for every cropped region.</p>
    <span class="step-tag">Python · custom tool</span>
  </div>
  <div class="step-card">
    <div class="step-num">03</div>
    <p class="step-title">Selection & Correction</p>
    <p class="step-desc">Annotators select the most accurate of the three OCR candidates and edit to ground truth. 10% of samples underwent double-blind review by independent linguists.</p>
    <span class="step-tag">κ > 0.85 IAA</span>
  </div>
</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── PHASE II ────────────────────────────────────────────────────────────────
with tab_p2:
    st.markdown('<div class="wrap" style="padding-top:32px;padding-bottom:48px;">', unsafe_allow_html=True)
    st.markdown(f'<span class="sec-label sec-label-g">Pipeline Performance</span>', unsafe_allow_html=True)
    m1,m2,m3,m4,m5=st.columns(5,gap="small")
    for cm,num,lbl,sub,g in [
        (m1,"97.6%","Age F1","rule-based",False),(m2,"83.8%","Height F1","rule-based",False),
        (m3,"58.2%","Education F1","LLM-assisted",False),(m4,"65.5%","Overall F1","hybrid pipeline",False),
        (m5,"+21%","vs baseline","hybrid gain",True)]:
        with cm:
            cls="metric-num metric-num-g" if g else "metric-num"
            st.markdown(f'<div class="metric-cell"><span class="{cls}">{num}</span><span class="metric-lbl">{lbl}</span><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    bl,br=st.columns(2,gap="large")
    with bl:
        st.markdown(f'<span class="sub-label">Hybrid Extraction Pipeline</span>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:14.5px;color:{IS};line-height:1.75;margin-bottom:16px;">A rule-based extractor handles high-precision fields while a Mistral LLM handles fields requiring linguistic understanding. Results are merged and exported as structured JSON per advertisement.</p>', unsafe_allow_html=True)
        st.markdown(f"""
<table class="method-table">
  <tr><td>Age · Height · Role</td><td><span class="tag-rule">RULE</span></td></tr>
  <tr><td>Caste · Box Number</td><td><span class="tag-rule">RULE</span></td></tr>
  <tr><td>Education · Profession</td><td><span class="tag-llm">LLM</span></td></tr>
  <tr><td>Other preferences</td><td><span class="tag-llm">LLM</span></td></tr>
</table>""", unsafe_allow_html=True)
        st.markdown(f'<br><span class="sub-label">SPARQL Query Examples</span>', unsafe_allow_html=True)
        qc1,qc2=st.columns(2,gap="small")
        for col,(qn,qt,qd) in zip([qc1,qc2,qc1,qc2],[
            ("Query ①","All Grooms: age, caste, education","Returns all Groom instances with optional age, caste name and education level, ordered by age."),
            ("Query ②","Age distribution","Groups all persons by age and counts instances, feeds the age distribution bar chart."),
            ("Query ③","Grooms aged 30+","Filters grooms with age ≥ 30 and joins education and profession data."),
            ("Query ④","Caste-no-bar preferences","Identifies advertisers whose requirement node carries a no-bar caste preference."),
        ]):
            with col:
                st.markdown(f'<div class="q-card"><span class="q-num">{qn}</span><span class="q-title">{qt}</span><span class="q-desc">{qd}</span></div>', unsafe_allow_html=True)
    with br:
        st.markdown(f'<span class="sub-label">OWL Ontology Schema</span>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:14.5px;color:{IS};line-height:1.75;margin-bottom:16px;">Extracted entities populate an OWL ontology enabling SPARQL-based querying of socio-cultural patterns across the corpus.</p>', unsafe_allow_html=True)
        # OWL schema formatted to match the HTML reference:
        # heading inline-left, content flows right, each entry on own line
        def sh(t): return f'<span style="color:{ACS};font-weight:600;">{t}</span>'
        def sk(t): return f'<span style="color:{RL};">{t}</span>'
        def sv(t): return f'<span style="color:{CA};opacity:.75;">{t}</span>'

        owl_content = (
            f'{sh("Classes")}\n'
            f'  {sk("Thing")}  →  {sv("Advertisement · Person · Requirement")}\n'
            f'  {sk("Person")}  →  {sv("Groom · Bride")}\n\n'

            f'{sh("Object Properties")}\n'
            f'  {sk("Advertisement")}  —{sv("advertises")}→  {sv("Person")}\n'
            f'  {sk("Person")}  —{sv("seeks")}→  {sv("Person")}\n'
            f'  {sk("Person")}  —{sv("hasRequirement")}→  {sv("Requirement")}\n\n'

            f'{sh("Data Properties")}\n'
            f'  {sk("Person")}      {sv("hasAge · hasHeight")}\n'
            f'               {sv("hasCasteName · hasEducationLevel")}\n'
            f'               {sv("hasProfession")}\n'
            f'  {sk("Ad")}          {sv("hasBoxNumber")}\n'
            f'  {sk("Requirement")} {sv("preferredAgeMin · preferredAgeMax")}\n'
            f'               {sv("preferredCaste")}'
        )
        st.markdown(dark_code(owl_content), unsafe_allow_html=True)
        st.markdown(f'<p style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{RU};margin-top:10px;">Serialisation: RDF/XML (.owl) · Queried via rdflib SPARQL engine</p>', unsafe_allow_html=True)

    # ── Live interface ──
    st.markdown(f"""
<div style="margin-top:40px;padding-top:36px;border-top:2px solid {INK};">
  <span class="sec-label sec-label-g">Live Research Interface</span>
  <h2 class="sec-heading">Interactive Pipeline</h2>
  <p class="sec-intro">Load your dataset, run hybrid NLP extraction, build the OWL ontology, explore the knowledge graph, and run SPARQL queries — all in one place.</p>
</div>""", unsafe_allow_html=True)

    ri1,ri2,ri3,ri4=st.tabs(["Dataset","Extraction","Knowledge Graph","SPARQL Queries"])

    with ri1:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<span class="sub-label">Data Sources</span>', unsafe_allow_html=True)
        dl,dr=st.columns(2,gap="large")
        with dl:
            st.markdown(f'<p style="font-size:14px;color:{IS};margin-bottom:12px;">Load annotated dataset</p>', unsafe_allow_html=True)
            if os.path.exists(DEFAULT_JSON_PATH):
                st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{IS};margin-bottom:10px;">{DEFAULT_JSON_PATH}</div>', unsafe_allow_html=True)
                if st.button("Load Cleaned Dataset"):
                    with open(DEFAULT_JSON_PATH,'r',encoding='utf-8') as f: ads=json.load(f)
                    st.session_state.raw_ads=ads; st.session_state.loaded=True
                    st.success(f"Loaded {len(ads)} advertisements."); st.rerun()
            else:
                up=st.file_uploader("Upload JSON dataset",type=['json'],key="jup")
                if up and st.button("Load Uploaded Dataset"):
                    ads=json.load(up); st.session_state.raw_ads=ads; st.session_state.loaded=True
                    st.success(f"Loaded {len(ads)} advertisements."); st.rerun()
            if st.session_state.loaded:
                st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{GR};margin-top:8px;">● {len(st.session_state.raw_ads)} ads ready</div>', unsafe_allow_html=True)
        with dr:
            st.markdown(f'<p style="font-size:14px;color:{IS};margin-bottom:12px;">Add individual ad <em>(paste raw OCR text)</em></p>', unsafe_allow_html=True)
            new_text=st.text_area("Ad text:",height=130,
                                   placeholder="Bengali Brahmin groom, 28/5'-6\", B.Tech...\nBox 2250",
                                   label_visibility="collapsed")
            if st.button("Add Ad to Dataset") and new_text.strip():
                nid=len(st.session_state.raw_ads)+1
                st.session_state.raw_ads.append({"id":nid,"raw_text":new_text.strip()})
                st.session_state.loaded=True
                st.success(f"Added as Ad #{nid}. Total: {len(st.session_state.raw_ads)}")
        if st.session_state.loaded and st.session_state.raw_ads:
            st.markdown(f'<br><span class="sub-label">Preview</span>', unsafe_allow_html=True)
            # preview_rows=[{"ID":str(a.get("id",i+1)),"Text Preview":str(a.get("raw_text",""))[:90]+"…"}
            #               for i,a in enumerate(st.session_state.raw_ads[:10])]
            # st.markdown(render_html_table(preview_rows), unsafe_allow_html=True)
            preview_rows=[{"ID":str(a.get("id",i+1)),"Text Preview":str(a.get("raw_text",""))[:90]+"…"}
              for i,a in enumerate(st.session_state.raw_ads)]
            st.markdown(
                f'<div style="max-height:360px;overflow-y:auto;border:1px solid {RL};">'
                + render_html_table(preview_rows) +
                '</div>', unsafe_allow_html=True)

    with ri2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<span class="sub-label">Hybrid Extraction Pipeline</span>', unsafe_allow_html=True)
        if not st.session_state.loaded:
            st.info("Load a dataset first in the Dataset tab.")
        else:
            ea,eb=st.columns([2,1],gap="large")
            with ea:
                use_llm=st.checkbox("Use Mistral LLM for Education / Profession fields",value=True)
                n_proc=st.slider("Ads to process",1,max(1,len(st.session_state.raw_ads)),
                                  min(len(st.session_state.raw_ads),25))
                if st.button("Run Extraction"):
                    ext=HybridExtractor(use_llm=use_llm); results=[]; pg=st.progress(0); st_=st.empty()
                    for i,ad in enumerate(st.session_state.raw_ads[:n_proc]):
                        st_.markdown(f'<span style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{IS};">Processing {i+1}/{n_proc}…</span>', unsafe_allow_html=True)
                        results.append(ext.extract(ad.get('raw_text',''),use_llm=use_llm))
                        pg.progress((i+1)/n_proc)
                        if use_llm: time.sleep(0.25)
                    st_.empty(); st.session_state.extractions=results
                    st.success(f"Extracted {len(results)} ads."); st.rerun()
            with eb:
                st.markdown(f"""
<div style="background:{CA};border:1px solid {RL};border-left:3px solid {AC};padding:22px 18px;">
  <p style="font-family:'Source Serif 4',serif;font-size:15px;font-weight:600;color:{GR};
     margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid {RL};">Method Key</p>
  <table class="method-table">
    <tr><td>Age · Height · Role</td><td><span class="tag-rule">RULE</span></td></tr>
    <tr><td>Caste · Box Number</td><td><span class="tag-rule">RULE</span></td></tr>
    <tr><td>Education · Profession</td><td><span class="tag-llm">LLM</span></td></tr>
    <tr><td>Other preferences</td><td><span class="tag-llm">LLM</span></td></tr>
  </table>
</div>""", unsafe_allow_html=True)
        if st.session_state.extractions:
            st.markdown(f'<br><span class="sub-label">Results — {len(st.session_state.extractions)} ads</span>', unsafe_allow_html=True)
            rows=[{"#":str(i+1),"Role":e['advertiser'].get('role','?'),
                   "Age":str(e['advertiser'].get('age','—')),"Height":str(e['advertiser'].get('height','—')),
                   "Caste":str(e['advertiser'].get('caste','—')),"Education":str(e['advertiser'].get('education','—')),
                   "Profession":str(e['advertiser'].get('profession','—'))} for i,e in enumerate(st.session_state.extractions)]
            st.markdown(render_html_table(rows), unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.download_button("Download extractions (JSON)",
                               data=json.dumps(st.session_state.extractions,indent=2,ensure_ascii=False),
                               file_name="extractions.json",mime="application/json")

    with ri3:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<span class="sub-label">OWL Ontology & Knowledge Graph</span>', unsafe_allow_html=True)
        if not st.session_state.extractions:
            st.info("Run extraction first in the Extraction tab.")
        else:
            kg1,kg2=st.columns([3,1],gap="large")
            with kg2:
                sidebar_owl = (
                    f'<span style="color:{ACS};font-weight:600;">Classes</span>\n'
                    f'  <span style="color:{RL};">Thing · Ad</span>\n'
                    f'  <span style="color:{RL};">Person · Req</span>\n'
                    f'  <span style="color:{RL};">Groom · Bride</span>\n\n'
                    f'<span style="color:{ACS};font-weight:600;">Obj Props</span>\n'
                    f'  <span style="color:{CA};">advertises</span>\n'
                    f'  <span style="color:{CA};">seeks</span>\n'
                    f'  <span style="color:{CA};">hasRequirement</span>\n\n'
                    f'<span style="color:{ACS};font-weight:600;">Data (9)</span>\n'
                    f'  <span style="color:{CA};">hasAge · hasHeight</span>\n'
                    f'  <span style="color:{CA};">hasCasteName</span>\n'
                    f'  <span style="color:{CA};">hasEducation</span>\n'
                    f'  <span style="color:{CA};">hasProfession</span>\n'
                    f'  <span style="color:{CA};">hasBoxNumber</span>\n'
                    f'  <span style="color:{CA};">prefAgeMin/Max</span>\n'
                    f'  <span style="color:{CA};">prefCaste</span>'
                )
                st.markdown(
                    f'<div style="background:{CA};border:1px solid {RL};border-left:3px solid {GR};padding:16px 14px;">'
                    + dark_code(sidebar_owl, "font-size:10.5px;") +
                    '</div>', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)
                if st.button("Build OWL Ontology"):
                    with st.spinner("Building OWL…"):
                        try:
                            path=build_ontology(st.session_state.extractions)
                            st.session_state.owl_path=path; st.success("Ontology built!"); st.rerun()
                        except Exception as ex: st.error(f"Error: {ex}")
                if st.session_state.owl_path:
                    st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{GR};margin-bottom:10px;">● OWL ready</div>', unsafe_allow_html=True)
                    with open(st.session_state.owl_path,'rb') as f:
                        st.download_button("Download .owl",data=f,
                                           file_name="matrimonial_ontology.owl",mime="application/rdf+xml")
            with kg1:
                kgt1,kgt2=st.tabs(["Interactive Graph","Ontology Hierarchy"])
                with kgt1:
                    try:
                        html=kg_pyvis(st.session_state.extractions)
                        if html: components.html(html,height=540,scrolling=False)
                        else: st.warning("Install pyvis: `pip install pyvis`")
                    except Exception as ex: st.error(f"Graph error: {ex}")
                with kgt2:
                    if st.session_state.owl_path:
                        try:
                            fig=ontology_fig(st.session_state.extractions)
                            st.pyplot(fig,use_container_width=True)
                            buf=io.BytesIO(); fig.savefig(buf,format='png',dpi=180,bbox_inches='tight',facecolor=CA); buf.seek(0)
                            st.download_button("Download diagram (PNG)",data=buf,file_name="ontology_diagram.png",mime="image/png")
                        except Exception as ex: st.error(f"Diagram error: {ex}")
                    else:
                        st.info("Build ontology first using the button →")
            n_g=sum(1 for e in st.session_state.extractions if e['advertiser'].get('role')=='groom')
            n_b=len(st.session_state.extractions)-n_g
            n_r=sum(1 for e in st.session_state.extractions if e['requirements'].get('caste_preference') or e['requirements'].get('age_max'))
            st.markdown('<br>', unsafe_allow_html=True)
            ga,gb,gc,gd=st.columns(4,gap="small")
            for cm,num,lbl,sub in [(ga,len(st.session_state.extractions),"Advertisements","OWL instances"),
                                    (gb,n_g,"Groom instances",""),(gc,n_b,"Bride instances",""),
                                    (gd,n_r,"Requirement nodes","with constraints")]:
                with cm:
                    st.markdown(f'<div class="metric-cell"><span class="metric-num">{num}</span><span class="metric-lbl">{lbl}</span><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)

    with ri4:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<span class="sub-label">SPARQL Semantic Query Interface</span>', unsafe_allow_html=True)
        if not st.session_state.owl_path:
            st.info("Build the ontology first in the Knowledge Graph tab.")
        else:
            sl,sr=st.columns([1,1],gap="large")
            with sl:
                sel=st.selectbox("Query template",list(SPARQL_QUERIES.keys()),label_visibility="collapsed")
                qt=st.text_area("SPARQL Editor",value=SPARQL_QUERIES[sel],height=300,label_visibility="collapsed")
                rb=st.button("Execute Query")
                if st.session_state.last_df is not None and not st.session_state.last_df.empty:
                    st.download_button("Export CSV",
                                       data=st.session_state.last_df.to_csv(index=False),
                                       file_name="sparql_results.csv",mime="text/csv")
            with sr:
                if rb:
                    with st.spinner("Running query…"):
                        df=run_sparql(st.session_state.owl_path,qt)
                        st.session_state.last_df=df
                if st.session_state.last_df is not None:
                    df=st.session_state.last_df
                    if not df.empty:
                        st.markdown(f'<span class="sub-label">{len(df)} result{"s" if len(df)!=1 else ""}</span>', unsafe_allow_html=True)
                        st.markdown(render_html_table(df), unsafe_allow_html=True)
                        if 'age' in df.columns and 'count' in df.columns:
                            fig2,ax2=plt.subplots(figsize=(8,3.5))
                            fig2.patch.set_facecolor(CA); ax2.set_facecolor(P)
                            counts=pd.to_numeric(df['count'],errors='coerce').fillna(0)
                            ax2.bar(df['age'].astype(str),counts,color=AC,width=0.7,alpha=0.9,edgecolor=ACS,linewidth=1.5)
                            ax2.set_xlabel("Age",color=INK,fontsize=10,fontweight='bold')
                            ax2.set_ylabel("Count",color=INK,fontsize=10,fontweight='bold')
                            ax2.tick_params(colors=IS,labelsize=9)
                            for sp in ax2.spines.values(): sp.set_color(RL); sp.set_linewidth(1.5)
                            ax2.set_title("Age Distribution",color=GR,fontsize=12,fontfamily="serif",fontweight='bold')
                            ax2.grid(axis='y',alpha=0.3,color=RL)
                            plt.tight_layout(); st.pyplot(fig2,use_container_width=True)
                    else:
                        st.warning("No results returned.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DELIVERABLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec"><div class="wrap">', unsafe_allow_html=True)
st.markdown(f"""
<span class="sec-label">Deliverables</span>
<h2 class="sec-heading">Proposed outcomes</h2>
<p class="sec-intro">An integrated knowledge portal serves as the primary deliverable — an invaluable resource offering insights into cultural practices and transitions in Bengali wedding and marriage practices over time.</p>
<div class="del-row">
  <div class="del-card"><div class="del-num">01</div><p class="del-title">Research Publications</p><p class="del-desc">Findings and insights disseminated through academic publications in reputable journals and presentations at conferences.</p></div>
  <div class="del-card"><div class="del-num">02</div><p class="del-title">Conferences & Workshops</p><p class="del-desc">Bringing together experts, scholars, and stakeholders in cultural studies, history, and digital humanities.</p></div>
  <div class="del-card"><div class="del-num">03</div><p class="del-title">Open Knowledge Portal</p><p class="del-desc">An integrated, publicly accessible portal presenting the annotated corpus, ontology, and query interface for ongoing scholarly use.</p></div>
</div>""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TEAM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec"><div class="wrap">', unsafe_allow_html=True)
st.markdown('<span class="sec-label">Research Team</span><h2 class="sec-heading">Principal Investigators</h2>', unsafe_allow_html=True)
pi_list=[
    ("images/principal_investigators/mayurakshi.jpg","Mayurakshi Chaudhuri"," ","Associate Professor of Sociology and Digital Humanities<br>FLAME University, Pune"),
    ("images/principal_investigators/shrimoyee.jpg","Shrimoyee Guha Thakurta <em>(nee Basu)</em>"," ","Associate Professor of History<br>Scottish Church College, Calcutta University"),
    ("images/principal_investigators/chiranjoy.jpg","Chiranjoy Chattopadhyay"," ","Associate Professor of Computer Science<br>FLAME University, Pune"),
]
for col,(img,name,role,inst) in zip(st.columns(3,gap="large"),pi_list):
    with col:
        show_img(img)
        st.markdown(f'<div class="pi-card"><p class="pi-name">{name}</p><p class="pi-role">{role}</p><p class="pi-inst">{inst}</p></div>', unsafe_allow_html=True)
st.markdown('<h2 class="sec-heading" style="margin-top:48px;">Project Associates</h2>', unsafe_allow_html=True)
assoc_list=[
    ("images/project_associates/amisha.jpeg","Amisha Mishra"," ","Research Associate<br>FLAME University, Pune"),
    ("images/project_associates/chaitri.jpg","Chaitri Nair"," ","Alumni<br>FLAME University, Pune"),
    ("images/project_associates/saptarsha.png","Saptarsha"," ","PhD Student<br>Jawaharlal Nehru University, New Delhi"),
]
for col,(img,name,role,inst) in zip(st.columns(3,gap="large"),assoc_list):
    with col:
        show_img(img)
        st.markdown(f'<div class="pi-card"><p class="pi-name">{name}</p><p class="pi-role">{role}</p><p class="pi-inst">{inst}</p></div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div id="contact" class="sec"><div class="wrap">', unsafe_allow_html=True)
st.markdown(f"""
<span class="sec-label">Reach Out</span>
<h2 class="sec-heading">Get in touch</h2>
<p class="sec-intro">For questions, collaboration enquiries, or data-sharing requests related to the PORINOY project, please get in touch with the research team.</p>
<div class="contact-block">
  <div class="contact-dot"></div>
  <div>
    <span class="contact-label">Email Address</span>
    <a href="mailto:mayurakshi.chaudhuri@flame.edu.in" class="contact-email" style="text-decoration:none!important;">mayurakshi.chaudhuri@flame.edu.in</a>
  </div>
</div>""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  <div class="wrap">
    PORINOY — IIT Indore &middot; JP Narayan National Centre of Excellence in Humanities
  </div>
</div>""", unsafe_allow_html=True)