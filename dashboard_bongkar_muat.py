import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Logistics Intelligence Dashboard",
    layout="wide",
    page_icon="🚢",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — DARK DEEP OCEAN THEME (ENHANCED)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;700;800&display=swap');

:root {
  --bg-root:     #040d18;
  --bg-navy:     #071628;
  --bg-card:     #0b1f35;
  --accent:      #00d4ff;
  --accent2:     #00e5a0;
  --accent3:     #7b5ea7;
  --warn:        #ff9f43;
  --danger:      #ff6b6b;
  --text:        #daeaf8;
  --muted:       #5d8aad;
  --border:      rgba(0,212,255,0.14);
  --glow-sm:     0 0 16px rgba(0,212,255,0.10);
  --glow-md:     0 0 28px rgba(0,212,255,0.18);
  --glow-lg:     0 0 48px rgba(0,212,255,0.22);
  --radius-lg:   18px;
  --radius-md:   12px;
}

html, body, .stApp {
  background-color: var(--bg-root) !important;
  color: var(--text) !important;
  font-family: 'Exo 2', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 1.2rem 2.2rem 4rem !important;
  max-width: 1700px !important;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #030c18 0%, #071422 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: var(--text) !important; }

[data-testid="metric-container"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  box-shadow: none !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text) !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
  background: rgba(0,212,255,0.18) !important;
  color: var(--accent) !important;
}

/* ── ENHANCED DataFrame Styling ── */
[data-testid="stDataFrame"] {
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--border) !important;
  overflow: hidden !important;
  box-shadow: var(--glow-sm) !important;
}
[data-testid="stDataFrame"] table {
  border-collapse: collapse !important;
}
[data-testid="stDataFrame"] thead tr th {
  background: linear-gradient(135deg, rgba(0,212,255,0.18), rgba(0,229,160,0.12)) !important;
  color: var(--accent) !important;
  font-weight: 700 !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  border-bottom: 1px solid rgba(0,212,255,0.25) !important;
  padding: 0.65rem 0.9rem !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(odd) td {
  background: rgba(7, 22, 40, 0.85) !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td {
  background: rgba(11, 31, 53, 0.85) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
  background: rgba(0,212,255,0.07) !important;
}
[data-testid="stDataFrame"] tbody tr td {
  color: #c4ddf0 !important;
  font-size: 0.82rem !important;
  border-bottom: 1px solid rgba(255,255,255,0.04) !important;
  padding: 0.5rem 0.9rem !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-root); }
::-webkit-scrollbar-thumb { background: #1a4060; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ─── Page Header ─── */
.pg-header {
  background: linear-gradient(120deg, #071628 0%, #0d2a45 50%, #071628 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 1.8rem 2.2rem;
  margin-bottom: 1.8rem;
  position: relative;
  overflow: hidden;
}
.pg-header::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 80% at 90% 50%, rgba(0,212,255,0.06), transparent);
  pointer-events: none;
}
.pg-header h1 {
  font-size: 1.75rem !important;
  font-weight: 800 !important;
  color: #fff !important;
  margin: 0 !important;
  font-family: 'Rajdhani', sans-serif !important;
  letter-spacing: 0.03em;
}
.pg-header p { color: var(--muted) !important; margin: 0.3rem 0 0 !important; font-size: 0.88rem !important; }
.badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(0,229,160,0.15));
  border: 1px solid rgba(0,212,255,0.3);
  color: var(--accent);
  font-size: 0.7rem; font-weight: 700;
  padding: 0.2rem 0.8rem;
  border-radius: 20px; text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 0.7rem;
}

/* ─── Section Title ─── */
.sec-title {
  display: flex; align-items: center; gap: 0.55rem;
  font-size: 0.78rem; font-weight: 700;
  color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.1em;
  padding-bottom: 0.7rem;
  margin: 0.4rem 0 1rem;
  border-bottom: 1px solid var(--border);
}
.sec-title span { color: var(--accent); font-size: 1rem; }

/* ─── KPI Card ─── */
.kpi {
  background: linear-gradient(145deg, var(--bg-card) 0%, #071424 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.3rem 1.5rem;
  box-shadow: var(--glow-sm);
  height: 100%;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.kpi:hover { transform: translateY(-4px); box-shadow: var(--glow-md); }
.kpi::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: 3px 3px 0 0;
}
.kpi-cyan::before   { background: linear-gradient(90deg, var(--accent), transparent); }
.kpi-green::before  { background: linear-gradient(90deg, var(--accent2), transparent); }
.kpi-purple::before { background: linear-gradient(90deg, var(--accent3), transparent); }
.kpi-warn::before   { background: linear-gradient(90deg, var(--warn), transparent); }
.kpi-danger::before { background: linear-gradient(90deg, var(--danger), transparent); }
.kpi-icon  { font-size: 1.5rem; margin-bottom: 0.5rem; }
.kpi-label { font-size: 0.68rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem; }
.kpi-value { font-size: 1.9rem; font-weight: 800; line-height: 1; margin-bottom: 0.3rem; font-family: 'Rajdhani', sans-serif; }
.kpi-cyan   .kpi-value { color: var(--accent); }
.kpi-green  .kpi-value { color: var(--accent2); }
.kpi-purple .kpi-value { color: #b39ddb; }
.kpi-warn   .kpi-value { color: var(--warn); }
.kpi-danger .kpi-value { color: var(--danger); }
.kpi-sub { font-size: 0.74rem; color: var(--muted); }
.kpi-tag {
  position: absolute; top: 1rem; right: 1rem;
  font-size: 0.62rem; font-weight: 700; color: var(--muted);
  background: rgba(255,255,255,0.05);
  border-radius: 6px; padding: 0.15rem 0.45rem;
  text-transform: uppercase; letter-spacing: 0.06em;
}

/* ─── ENHANCED Chart Card ─── */
.ch-card {
  background: linear-gradient(145deg, #0b1f35 0%, #071424 60%, #050e1c 100%);
  border: 1px solid rgba(0,212,255,0.18);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.4rem 0.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(0,212,255,0.06) inset;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
}
/* Subtle corner glow decorations */
.ch-card::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 120px; height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
  pointer-events: none;
}
.ch-card::after {
  content: '';
  position: absolute;
  bottom: -30px; left: -30px;
  width: 90px; height: 90px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,229,160,0.05) 0%, transparent 70%);
  pointer-events: none;
}

/* Green-tinted card */
.ch-card-green {
  background: linear-gradient(145deg, #0b2030 0%, #071e20 60%, #050e14 100%);
  border-color: rgba(0,229,160,0.18);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(0,229,160,0.06) inset;
}
.ch-card-green::before {
  background: radial-gradient(circle, rgba(0,229,160,0.07) 0%, transparent 70%);
}
/* Purple-tinted card */
.ch-card-purple {
  background: linear-gradient(145deg, #0f1630 0%, #0a1025 60%, #060914 100%);
  border-color: rgba(123,94,167,0.22);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(123,94,167,0.07) inset;
}
.ch-card-purple::before {
  background: radial-gradient(circle, rgba(123,94,167,0.09) 0%, transparent 70%);
}
/* Warn-tinted card */
.ch-card-warn {
  background: linear-gradient(145deg, #1a1508 0%, #130f04 60%, #080600 100%);
  border-color: rgba(255,159,67,0.18);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,159,67,0.06) inset;
}
/* Danger-tinted card */
.ch-card-danger {
  background: linear-gradient(145deg, #1a0a0a 0%, #130505 60%, #080000 100%);
  border-color: rgba(255,107,107,0.18);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,107,107,0.06) inset;
}

.ch-card-title {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.8rem; font-weight: 700;
  color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em;
  margin-bottom: 0.2rem; padding-bottom: 0.7rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.dot       { width:8px; height:8px; border-radius:50%; background:var(--accent);  box-shadow:0 0 6px var(--accent);  display:inline-block; flex-shrink:0; }
.dot-green  { background:var(--accent2) !important; box-shadow:0 0 6px var(--accent2) !important; }
.dot-purple { background:var(--accent3) !important; box-shadow:0 0 6px var(--accent3) !important; }
.dot-warn   { background:var(--warn) !important;    box-shadow:0 0 6px var(--warn) !important; }
.dot-danger { background:var(--danger) !important;  box-shadow:0 0 6px var(--danger) !important; }

/* ─── Filter Card ─── */
.filter-card {
  background: rgba(11,31,53,0.7);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.2rem 0.2rem;
  margin-bottom: 1rem;
}

/* ─── Info Pills ─── */
.info-pill {
  background: rgba(0,229,160,0.08);
  border-left: 3px solid var(--accent2);
  border-radius: 0 10px 10px 0;
  padding: 0.65rem 1rem;
  font-size: 0.82rem; color: #a0d8cc;
  margin-top: 0.6rem; margin-bottom: 0.4rem;
}
.warn-pill {
  background: rgba(255,159,67,0.08);
  border-left: 3px solid var(--warn);
  border-radius: 0 10px 10px 0;
  padding: 0.65rem 1rem;
  font-size: 0.82rem; color: #d4b483;
  margin-top: 0.6rem;
}

/* ─── HR Divider ─── */
.hr-div {
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(0,212,255,0.25) 40%, rgba(0,229,160,0.2) 60%, transparent 100%);
  border: none; margin: 2rem 0;
}

/* ─── Sidebar Nav ─── */
.nav-logo { font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 1.1rem; }
.nav-link {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.55rem 0.9rem; border-radius: 9px;
  font-size: 0.87rem; font-weight: 600; color: var(--muted);
  margin-bottom: 0.25rem;
  border-left: 3px solid transparent;
}
.nav-link.active { background: rgba(0,212,255,0.1); color: var(--accent); border-left-color: var(--accent); }

/* ─── Footer ─── */
.footer { text-align: center; padding: 2.5rem 0 1rem; color: #2d5070; font-size: 0.78rem; }
.footer strong { color: var(--muted); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY HELPERS
# ─────────────────────────────────────────────
PAL = ['#00d4ff','#00e5a0','#7b5ea7','#ff9f43','#ff6b6b',
       '#42a5f5','#66bb6a','#ab47bc','#ffa726','#26c6da']

def dark_fig(fig, h=350):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c4ddf0', family='Exo 2', size=11),
        height=h,
        margin=dict(l=6, r=6, t=8, b=6),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)',
                   tickcolor='rgba(255,255,255,0.15)', color='#5d8aad'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)',
                   tickcolor='rgba(255,255,255,0.15)', color='#5d8aad'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8ab5cc', size=10),
                    bordercolor='rgba(255,255,255,0.07)', borderwidth=1),
    )
    return fig

def hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'

def card_open(title, dot_cls="", card_cls=""):
    """Open a chart card with optional color variant and dot color."""
    st.markdown(f"""
    <div class="ch-card {card_cls}">
      <div class="ch-card-title">
        <span class="dot {dot_cls}"></span>{title}
      </div>
    """, unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0.5rem 0.5rem;text-align:center;">
      <div style="font-size:2.4rem;">🚢</div>
      <div class="nav-logo" style="color:#daeaf8;margin:0.3rem 0 0.1rem;">LOGISTICS HUB</div>
      <div style="font-size:0.67rem;color:#3a6480;text-transform:uppercase;letter-spacing:0.12em;">Intelligence Dashboard v2.2</div>
      <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.25),transparent);margin:1rem 0;"></div>
    </div>
    <div style="font-size:0.68rem;color:#3a6480;text-transform:uppercase;letter-spacing:0.1em;padding:0 0.2rem 0.4rem;">Navigasi</div>
    <div class="nav-link active">📊 &nbsp;KPI Utama</div>
    <div class="nav-link">📈 &nbsp;Ringkasan Eksekutif</div>
    <div class="nav-link">📆 &nbsp;Tren &amp; Musiman</div>
    <div class="nav-link">🏠 &nbsp;Analisis Dasar</div>
    <div class="nav-link">📦 &nbsp;Komoditas Unggulan</div>
    <div class="nav-link">⚖️ &nbsp;Keseimbangan Perdagangan</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.68rem;color:#3a6480;text-transform:uppercase;letter-spacing:0.1em;padding:0 0 0.4rem;">Pengaturan</div>', unsafe_allow_html=True)
    chart_h  = st.slider("Tinggi Grafik (px)", 280, 520, 360, 20)
    show_raw = st.checkbox("Tampilkan Tabel Data", value=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#2a4a60;text-align:center;padding:0.4rem 0 1rem;">
      <span style="color:#00d4ff;">●</span> LIVE &nbsp;|&nbsp; Data aktif<br>
      <span style="color:#3a6480;">Logistics Intelligence System</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    file_path = 'BONGKAR_2.xlsx'
    xls   = pd.ExcelFile(file_path)
    names = xls.sheet_names
    t_b   = next((s for s in names if 'bongkar' in s.lower()), None)
    t_m   = next((s for s in names if 'muat'    in s.lower()), None)
    if not t_b or not t_m:
        raise ValueError(f"Sheet tidak lengkap! Ditemukan: {names}")
    df_b = pd.read_excel(file_path, sheet_name=t_b); df_b['Aktivitas'] = 'Bongkar'
    df_m = pd.read_excel(file_path, sheet_name=t_m); df_m['Aktivitas'] = 'Muat'
    df   = pd.concat([df_b, df_m], ignore_index=True)
    df['Berat'] = pd.to_numeric(df['Berat'], errors='coerce').fillna(0)
    return df

# ─────────────────────────────────────────────
# MONTH SORT HELPER
# ─────────────────────────────────────────────
BULAN_ID = {
    'januari':1,'februari':2,'maret':3,'april':4,
    'mei':5,'juni':6,'juli':7,'agustus':8,
    'september':9,'oktober':10,'november':11,'desember':12,
    # Short forms
    'jan':1,'feb':2,'mar':3,'apr':4,'jun':6,'jul':7,
    'agu':8,'sep':9,'okt':10,'nov':11,'des':12,
}

def bulan_sort_key(val):
    """Return a sortable (year, month) tuple from a Bulan value."""
    if pd.isna(val):
        return (9999, 99)
    s = str(val).strip().lower()
    # Try pure integer (month number)
    try:
        return (0, int(s))
    except ValueError:
        pass
    # Try "MMMM YYYY" or "YYYY MMMM" or "MMMM-YYYY"
    import re
    parts = re.split(r'[\s\-_/]+', s)
    year, month = 0, 0
    for p in parts:
        try:
            n = int(p)
            if 1000 <= n <= 9999:
                year = n
            elif 1 <= n <= 12:
                month = n
        except ValueError:
            if p in BULAN_ID:
                month = BULAN_ID[p]
    return (year, month if month else 99)

def sort_bulan_series(series):
    """Return a sorted list of unique Bulan values."""
    unique_vals = series.dropna().unique().tolist()
    return sorted(unique_vals, key=bulan_sort_key)

# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="pg-header">
  <div class="badge">🚢 Port Intelligence System &nbsp;●&nbsp; Real-Time Analytics</div>
  <h1>Dashboard Bongkar &amp; Muat</h1>
  <p>Analisis terpadu arus barang, komoditas, tren musiman, dan keseimbangan perdagangan pelabuhan</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
try:
    df = load_data()

    # ══════════════════════════════════════════
    # SECTION 1 — KPI SCORECARD
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>📊</span> KPI Utama</div>', unsafe_allow_html=True)

    vol_b      = df[df['Aktivitas'] == 'Bongkar']['Berat'].sum()
    vol_m      = df[df['Aktivitas'] == 'Muat']['Berat'].sum()
    throughput = vol_b + vol_m
    rasio      = vol_b / vol_m if vol_m > 0 else 0
    top_komo   = df.groupby('Komoditas')['Berat'].sum().idxmax()
    jml_komo   = df['Komoditas'].nunique()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="kpi kpi-cyan">
          <div class="kpi-tag">BONGKAR</div>
          <div class="kpi-icon">🔽</div>
          <div class="kpi-label">Total Bongkar</div>
          <div class="kpi-value">{vol_b:,.0f}</div>
          <div class="kpi-sub">Ton masuk ke pelabuhan</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi kpi-green">
          <div class="kpi-tag">MUAT</div>
          <div class="kpi-icon">🔼</div>
          <div class="kpi-label">Total Muat</div>
          <div class="kpi-value">{vol_m:,.0f}</div>
          <div class="kpi-sub">Ton keluar dari pelabuhan</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi kpi-purple">
          <div class="kpi-tag">TOTAL</div>
          <div class="kpi-icon">⚓</div>
          <div class="kpi-label">Total Throughput</div>
          <div class="kpi-value">{throughput:,.0f}</div>
          <div class="kpi-sub">Ton total pergerakan</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi kpi-warn">
          <div class="kpi-tag">RASIO</div>
          <div class="kpi-icon">⚖️</div>
          <div class="kpi-label">Rasio Bongkar/Muat</div>
          <div class="kpi-value">{rasio:.2f}x</div>
          <div class="kpi-sub">Indikator keseimbangan arus</div>
        </div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="kpi kpi-danger">
          <div class="kpi-tag">KOMODITAS</div>
          <div class="kpi-icon">🏆</div>
          <div class="kpi-label">Komoditas Dominan</div>
          <div class="kpi-value" style="font-size:1.1rem;line-height:1.3;">{top_komo}</div>
          <div class="kpi-sub">{jml_komo} jenis komoditas total</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="hr-div">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SECTION 2 — RINGKASAN EKSEKUTIF
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>📈</span> Ringkasan Eksekutif</div>', unsafe_allow_html=True)

    e1, e2, e3 = st.columns([1, 1.2, 1.2])

    # ── E1: Donut Komposisi Aktivitas ──
    with e1:
        card_open("Komposisi Aktivitas", "", "")
        act_sum = df.groupby('Aktivitas')['Berat'].sum().reset_index()
        fig_donut = go.Figure(go.Pie(
            labels=act_sum['Aktivitas'], values=act_sum['Berat'],
            hole=0.62,
            marker=dict(colors=['#00d4ff','#00e5a0'], line=dict(color='#040d18', width=3)),
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} Ton<br>%{percent}<extra></extra>',
        ))
        fig_donut.add_annotation(
            text=f"<b>{throughput/1e6:.1f}M</b><br>Ton Total",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color='#daeaf8', family='Rajdhani'), align='center',
        )
        dark_fig(fig_donut, h=chart_h)
        fig_donut.update_layout(legend=dict(orientation='h', y=-0.05, x=0.15))
        st.plotly_chart(fig_donut, use_container_width=True)
        card_close()

    # ── E2: Top 5 Komoditas Terbesar BONGKAR (menggantikan "Top 5 Terbesar" umum) ──
    with e2:
        card_open("Top 5 Komoditas Terbesar — Bongkar", "dot-cyan", "")
        top5_bongkar = (
            df[df['Aktivitas'] == 'Bongkar']
            .groupby('Komoditas')['Berat'].sum()
            .nlargest(5).reset_index().sort_values('Berat')
        )
        # Gradient bar colors cyan → teal
        bar_colors_bongkar = [
            '#004d6e', '#006d96', '#0094ba', '#00bcd4', '#00d4ff'
        ]
        fig_h5b = go.Figure()
        total_b5 = top5_bongkar['Berat'].sum()
        for i, row in top5_bongkar.iterrows():
            pct = row['Berat'] / total_b5 * 100
            color_idx = list(top5_bongkar.index).index(i)
            fig_h5b.add_trace(go.Bar(
                x=[row['Berat']], y=[row['Komoditas']],
                orientation='h', name=row['Komoditas'],
                marker=dict(
                    color=bar_colors_bongkar[color_idx],
                    line=dict(width=0),
                    opacity=0.92,
                ),
                text=f" {pct:.1f}%",
                textposition='outside',
                textfont=dict(color='#00d4ff', size=10, family='Exo 2'),
                hovertemplate='<b>%{y}</b><br>%{x:,.0f} Ton<extra></extra>',
            ))
        dark_fig(fig_h5b, h=chart_h)
        fig_h5b.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(0,212,255,0.07)'),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_h5b, use_container_width=True)
        card_close()

    # ── E3: Top 5 Komoditas Terbesar MUAT (menggantikan Funnel) ──
    with e3:
        card_open("Top 5 Komoditas Terbesar — Muat", "dot-green", "ch-card-green")
        top5_muat = (
            df[df['Aktivitas'] == 'Muat']
            .groupby('Komoditas')['Berat'].sum()
            .nlargest(5).reset_index().sort_values('Berat')
        )
        # Gradient bar colors green shades
        bar_colors_muat = [
            '#004d38', '#006b4f', '#00916b', '#00b888', '#00e5a0'
        ]
        fig_h5m = go.Figure()
        total_m5 = top5_muat['Berat'].sum()
        for i, row in top5_muat.iterrows():
            pct = row['Berat'] / total_m5 * 100
            color_idx = list(top5_muat.index).index(i)
            fig_h5m.add_trace(go.Bar(
                x=[row['Berat']], y=[row['Komoditas']],
                orientation='h', name=row['Komoditas'],
                marker=dict(
                    color=bar_colors_muat[color_idx],
                    line=dict(width=0),
                    opacity=0.92,
                ),
                text=f" {pct:.1f}%",
                textposition='outside',
                textfont=dict(color='#00e5a0', size=10, family='Exo 2'),
                hovertemplate='<b>%{y}</b><br>%{x:,.0f} Ton<extra></extra>',
            ))
        dark_fig(fig_h5m, h=chart_h)
        fig_h5m.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(0,229,160,0.07)'),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_h5m, use_container_width=True)
        card_close()

    st.markdown('<hr class="hr-div">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SECTION 3 — TREN & MUSIMAN
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>📆</span> Tren &amp; Musiman</div>', unsafe_allow_html=True)

    t1, t2 = st.columns([1.7, 1])
    df_time = df.groupby(['Bulan','Aktivitas'])['Berat'].sum().reset_index()
    # Build ordered Bulan category so all charts follow Jan→Dec order
    bulan_order = sort_bulan_series(df['Bulan'])
    df_time['Bulan'] = pd.Categorical(df_time['Bulan'], categories=bulan_order, ordered=True)
    df_time = df_time.sort_values('Bulan')

    with t1:
        card_open("Perbandingan Bulanan: Bongkar vs Muat (Spline Area)", "", "")
        fig_trend = go.Figure()
        for i, akt in enumerate(df_time['Aktivitas'].unique()):
            sub = df_time[df_time['Aktivitas'] == akt].sort_values('Bulan')
            fig_trend.add_trace(go.Scatter(
                x=sub['Bulan'].astype(str), y=sub['Berat'],
                mode='lines+markers', name=akt,
                line=dict(color=PAL[i], width=2.5, shape='spline'),
                marker=dict(size=7, color=PAL[i], line=dict(color='#040d18', width=2)),
                fill='tozeroy', fillcolor=hex_to_rgba(PAL[i], 0.07),
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} Ton<extra>' + akt + '</extra>',
            ))
        dark_fig(fig_trend, h=chart_h)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("""
        <div class="info-pill">
          💡 Grafik ini membantu pimpinan memprediksi <strong>Peak Season</strong> pelabuhan
          untuk perencanaan kapasitas, SDM, dan alokasi anggaran.
        </div>""", unsafe_allow_html=True)
        card_close()

    with t2:
        card_open("Volume per Bulan (Stacked Bar)", "dot-green", "ch-card-green")
        fig_mbar = go.Figure()
        for i, akt in enumerate(df_time['Aktivitas'].unique()):
            sub = df_time[df_time['Aktivitas'] == akt].sort_values('Bulan')
            fig_mbar.add_trace(go.Bar(
                x=sub['Bulan'].astype(str), y=sub['Berat'], name=akt,
                marker_color=PAL[i], marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} Ton<extra>' + akt + '</extra>',
            ))
        dark_fig(fig_mbar, h=chart_h)
        fig_mbar.update_layout(barmode='stack')
        st.plotly_chart(fig_mbar, use_container_width=True)
        card_close()

    st.markdown('<hr class="hr-div">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SECTION 4 — ANALISIS DASAR
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>🏠</span> Analisis Dasar Arus Barang</div>', unsafe_allow_html=True)

    all_komo = sorted(df['Komoditas'].unique().tolist())
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    sel_komo = st.multiselect("🔍 Filter Komoditas:", all_komo,
                               default=all_komo[:min(4, len(all_komo))], key="komo_main")
    st.markdown('</div>', unsafe_allow_html=True)

    df_f = df[df['Komoditas'].isin(sel_komo)] if sel_komo else df.copy()

    a1, a2 = st.columns(2)
    with a1:
        card_open("Tren Berat Per Bulan (Terfilter)", "", "")
        pv = df_f.pivot_table(index='Bulan', columns='Aktivitas', values='Berat', aggfunc='sum').reset_index()
        # Apply correct month ordering to pivot
        pv['Bulan'] = pd.Categorical(pv['Bulan'], categories=bulan_order, ordered=True)
        pv = pv.sort_values('Bulan')
        fig_fline = go.Figure()
        for i, col in enumerate([c for c in pv.columns if c != 'Bulan']):
            fig_fline.add_trace(go.Scatter(
                x=pv['Bulan'].astype(str), y=pv[col], mode='lines+markers', name=col,
                line=dict(color=PAL[i], width=2.5, shape='spline'),
                marker=dict(size=7, color=PAL[i], line=dict(color='#040d18', width=2)),
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} Ton<extra>' + col + '</extra>',
            ))
        dark_fig(fig_fline, h=chart_h)
        st.plotly_chart(fig_fline, use_container_width=True)
        card_close()

    with a2:
        card_open("Perbandingan Volume per Komoditas (Grouped)", "dot-green", "ch-card-green")
        bar_data = df_f.groupby(['Komoditas','Aktivitas'])['Berat'].sum().reset_index()
        fig_fbar = px.bar(bar_data, x='Komoditas', y='Berat', color='Aktivitas',
                          barmode='group', color_discrete_sequence=PAL)
        fig_fbar.update_traces(marker_line_width=0)
        dark_fig(fig_fbar, h=chart_h)
        st.plotly_chart(fig_fbar, use_container_width=True)
        card_close()

    if show_raw:
        card_open("📄 Tabel Data Terfilter", "dot-purple", "ch-card-purple")

        def style_berat(val):
            try:
                n = float(val)
                # Normalize color intensity based on value
                max_val = df_f['Berat'].max() if df_f['Berat'].max() > 0 else 1
                intensity = min(int(n / max_val * 180), 180)
                return f'color: rgb({80 + intensity//3}, {180 + intensity//6}, {255}); font-weight: 600'
            except:
                return ''

        styled_raw = (
            df_f.style
            .applymap(style_berat, subset=['Berat'])
            .set_properties(**{
                'font-size': '0.82rem',
                'border-color': 'rgba(0,212,255,0.10)',
            })
            .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', 'rgba(0,212,255,0.15)'),
                    ('color', '#00d4ff'),
                    ('font-weight', '700'),
                    ('text-transform', 'uppercase'),
                    ('letter-spacing', '0.07em'),
                    ('font-size', '0.72rem'),
                    ('border-bottom', '1px solid rgba(0,212,255,0.25)'),
                    ('padding', '0.6rem 0.9rem'),
                ]
            }, {
                'selector': 'tr:nth-child(odd) td',
                'props': [('background-color', 'rgba(7,22,40,0.85)')]
            }, {
                'selector': 'tr:nth-child(even) td',
                'props': [('background-color', 'rgba(11,31,53,0.85)')]
            }, {
                'selector': 'tr:hover td',
                'props': [('background-color', 'rgba(0,212,255,0.06)')]
            }, {
                'selector': 'td',
                'props': [
                    ('color', '#c4ddf0'),
                    ('border-bottom', '1px solid rgba(255,255,255,0.04)'),
                    ('padding', '0.45rem 0.9rem'),
                ]
            }])
        )
        st.dataframe(styled_raw, use_container_width=True, height=260)
        card_close()

    st.markdown('<hr class="hr-div">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SECTION 5 — KOMODITAS UNGGULAN
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>📦</span> Analisis Komoditas Unggulan</div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    komo_sel = st.selectbox("🔍 Pilih Komoditas Spesifik:", sorted(df['Komoditas'].unique()), key="komo_spec")
    st.markdown('</div>', unsafe_allow_html=True)

    df_sp = df[df['Komoditas'] == komo_sel]
    p1, p2, p3 = st.columns([1.2, 1, 1])

    with p1:
        card_open(f"Area Chart: {komo_sel}", "", "")
        fig_area = go.Figure()
        for i, akt in enumerate(df_sp['Aktivitas'].unique()):
            sub = df_sp[df_sp['Aktivitas'] == akt].copy()
            sub['Bulan'] = pd.Categorical(sub['Bulan'], categories=bulan_order, ordered=True)
            sub = sub.sort_values('Bulan')
            fig_area.add_trace(go.Scatter(
                x=sub['Bulan'].astype(str), y=sub['Berat'],
                mode='lines', name=akt,
                line=dict(color=PAL[i], width=2.5, shape='spline'),
                fill='tozeroy', fillcolor=hex_to_rgba(PAL[i], 0.15),
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} Ton<extra>' + akt + '</extra>',
            ))
        dark_fig(fig_area, h=chart_h)
        st.plotly_chart(fig_area, use_container_width=True)
        card_close()

    with p2:
        card_open("Pareto — Semua Komoditas", "dot-warn", "ch-card-warn")
        pareto = df.groupby('Komoditas')['Berat'].sum().sort_values(ascending=True).reset_index()
        colors_p = [PAL[0] if k == komo_sel else '#1a3d5c' for k in pareto['Komoditas']]
        fig_par = go.Figure(go.Bar(
            x=pareto['Berat'], y=pareto['Komoditas'],
            orientation='h',
            marker=dict(color=colors_p, line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>%{x:,.0f} Ton<extra></extra>',
        ))
        dark_fig(fig_par, h=chart_h)
        fig_par.update_layout(yaxis=dict(showgrid=False), xaxis=dict(showgrid=True))
        st.plotly_chart(fig_par, use_container_width=True)
        card_close()

    with p3:
        card_open("Radar — Top 6 Komoditas", "dot-purple", "ch-card-purple")
        top6_komo = df.groupby('Komoditas')['Berat'].sum().nlargest(6).index.tolist()
        df_r    = df[df['Komoditas'].isin(top6_komo)]
        radar_d = df_r.groupby(['Komoditas','Aktivitas'])['Berat'].sum().unstack(fill_value=0).reset_index()
        fig_rad = go.Figure()
        for i, akt in enumerate([c for c in radar_d.columns if c != 'Komoditas']):
            vals = radar_d[akt].tolist()
            cats = radar_d['Komoditas'].tolist()
            fig_rad.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=cats + [cats[0]],
                fill='toself', name=akt,
                line=dict(color=PAL[i], width=2),
                fillcolor=hex_to_rgba(PAL[i], 0.10),
            ))
        dark_fig(fig_rad, h=chart_h)
        fig_rad.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.07)',
                                color='#3a6480', showticklabels=False),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.07)', color='#5d8aad'),
            )
        )
        st.plotly_chart(fig_rad, use_container_width=True)
        card_close()

    st.markdown('<hr class="hr-div">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SECTION 6 — KESEIMBANGAN PERDAGANGAN
    # ══════════════════════════════════════════
    st.markdown('<div class="sec-title"><span>⚖️</span> Keseimbangan Perdagangan Regional</div>', unsafe_allow_html=True)

    df_pv = df.pivot_table(index='Komoditas', columns='Aktivitas', values='Berat', aggfunc='sum').fillna(0).reset_index()
    if 'Bongkar' not in df_pv.columns: df_pv['Bongkar'] = 0
    if 'Muat'    not in df_pv.columns: df_pv['Muat']    = 0

    df_pv['Gap']    = df_pv['Bongkar'] - df_pv['Muat']
    df_pv['AbsGap'] = df_pv['Gap'].abs()
    df_pv['Status'] = df_pv['Gap'].apply(lambda x: 'Surplus Masuk' if x >= 0 else 'Surplus Keluar')

    g1, g2 = st.columns([1.6, 1])

    with g1:
        card_open("Analisis Gap — Bongkar vs Muat per Komoditas (Color-coded Bar)", "", "")
        bar_colors = ['#00d4ff' if x >= 0 else '#ff6b6b' for x in df_pv['Gap']]
        fig_gap = go.Figure(go.Bar(
            x=df_pv['Komoditas'], y=df_pv['Gap'],
            marker=dict(color=bar_colors, line=dict(width=0), opacity=0.88),
            hovertemplate='<b>%{x}</b><br>Gap: %{y:,.0f} Ton<extra></extra>',
        ))
        fig_gap.add_hline(y=0, line_color='rgba(255,255,255,0.18)', line_width=1)
        dark_fig(fig_gap, h=chart_h)
        st.plotly_chart(fig_gap, use_container_width=True)
        st.markdown("""
        <div class="info-pill">
          📊 <span style="color:#00d4ff;font-weight:700;">Biru (positif)</span> = lebih banyak masuk (konsumsi) &nbsp;|&nbsp;
          <span style="color:#ff6b6b;font-weight:700;">Merah (negatif)</span> = lebih banyak keluar (produksi/ekspor)
        </div>""", unsafe_allow_html=True)
        card_close()

    with g2:
        card_open("Scatter: Bongkar vs Muat", "dot-warn", "ch-card-warn")
        abs_vals   = df_pv['AbsGap'].values
        max_abs    = abs_vals.max() if abs_vals.max() > 0 else 1
        size_vals  = (abs_vals / max_abs * 40 + 8).tolist()

        fig_sc = go.Figure(go.Scatter(
            x=df_pv['Bongkar'], y=df_pv['Muat'],
            mode='markers+text',
            text=df_pv['Komoditas'],
            textposition='top center',
            textfont=dict(size=8, color='#5d8aad'),
            marker=dict(
                size=size_vals,
                color=df_pv['Gap'],
                colorscale=[[0.0,'#ff6b6b'],[0.5,'#7b5ea7'],[1.0,'#00d4ff']],
                showscale=True,
                colorbar=dict(
                    title=dict(text='Gap', font=dict(color='#5d8aad', size=9)),
                    thickness=10, len=0.7,
                    tickfont=dict(color='#5d8aad', size=9),
                ),
                line=dict(color='#040d18', width=1),
                opacity=0.85,
            ),
            hovertemplate='<b>%{text}</b><br>Bongkar: %{x:,.0f}<br>Muat: %{y:,.0f}<extra></extra>',
        ))
        dark_fig(fig_sc, h=chart_h)
        st.plotly_chart(fig_sc, use_container_width=True)
        card_close()

    if show_raw:
        card_open("📋 Tabel Detail Keseimbangan Perdagangan", "dot-green", "ch-card-green")
        disp = df_pv[['Komoditas','Bongkar','Muat','Gap','Status']].copy()

        def color_gap(val):
            """Color positive gap cyan, negative red."""
            try:
                num = float(str(val).replace(',',''))
                if num > 0:
                    return 'color: #00d4ff; font-weight: 700'
                elif num < 0:
                    return 'color: #ff6b6b; font-weight: 700'
            except:
                pass
            return ''

        def color_status(val):
            if val == 'Surplus Masuk':
                return 'color: #00e5a0; font-weight: 600'
            elif val == 'Surplus Keluar':
                return 'color: #ff9f43; font-weight: 600'
            return ''

        def color_bongkar(val):
            return 'color: #00d4ff'

        def color_muat(val):
            return 'color: #00e5a0'

        styled_disp = (
            disp.style
            .format({'Bongkar': '{:,.0f}', 'Muat': '{:,.0f}', 'Gap': '{:,.0f}'})
            .applymap(color_bongkar, subset=['Bongkar'])
            .applymap(color_muat, subset=['Muat'])
            .applymap(color_gap, subset=['Gap'])
            .applymap(color_status, subset=['Status'])
            .set_properties(**{
                'background-color': 'rgba(7,22,40,0.0)',
                'border-color': 'rgba(0,212,255,0.10)',
                'font-size': '0.82rem',
            })
            .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', 'rgba(0,212,255,0.12)'),
                    ('color', '#00d4ff'),
                    ('font-weight', '700'),
                    ('text-transform', 'uppercase'),
                    ('letter-spacing', '0.06em'),
                    ('font-size', '0.72rem'),
                    ('border-bottom', '1px solid rgba(0,212,255,0.2)'),
                ]
            }, {
                'selector': 'tr:nth-child(odd)',
                'props': [('background-color', 'rgba(7,22,40,0.7)')]
            }, {
                'selector': 'tr:nth-child(even)',
                'props': [('background-color', 'rgba(11,31,53,0.7)')]
            }, {
                'selector': 'tr:hover',
                'props': [('background-color', 'rgba(0,212,255,0.06)')]
            }])
        )

        st.dataframe(styled_disp, use_container_width=True, height=250)
        st.markdown("""
        <div class="warn-pill">
          ⚠️ Data menampilkan akumulasi seluruh periode. Gunakan filter komoditas di atas
          untuk analisis lebih spesifik.
        </div>""", unsafe_allow_html=True)
        card_close()

    # Footer
    st.markdown("""
    <div class="footer">
      <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.15),transparent);margin-bottom:1.5rem;"></div>
      🚢 &nbsp;<strong>Logistics Intelligence Dashboard</strong> &nbsp;·&nbsp;
      Sumber: <code>BONGKAR_2.xlsx</code> &nbsp;·&nbsp;
      Dibangun dengan Streamlit &amp; Plotly &nbsp;·&nbsp; v2.2
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.markdown("""
    <div style="background:rgba(255,100,0,0.08);border:1px solid rgba(255,100,0,0.25);
                border-radius:18px;padding:2.5rem;text-align:center;margin-top:2rem;">
      <div style="font-size:3rem;margin-bottom:1rem;">📁</div>
      <div style="font-size:1.2rem;font-weight:700;color:#ff9966;margin-bottom:0.5rem;">File Data Tidak Ditemukan</div>
      <div style="color:#5d8aad;font-size:0.88rem;">
        Pastikan file <code style="background:rgba(255,255,255,0.08);padding:0.2rem 0.5rem;border-radius:4px;">BONGKAR_2.xlsx</code>
        tersedia di folder yang sama dengan script ini, lalu jalankan kembali.
      </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kendala: {e}")
    st.markdown("""
    <div style="background:rgba(255,159,67,0.08);border-left:3px solid #ff9f43;border-radius:0 10px 10px 0;
                padding:0.65rem 1rem;font-size:0.82rem;color:#d4b483;margin-top:0.6rem;">
      🛠️ Periksa struktur Excel: sheet harus mengandung kata <strong>'bongkar'</strong> dan <strong>'muat'</strong>,
      dengan kolom <strong>Berat</strong>, <strong>Bulan</strong>, dan <strong>Komoditas</strong>.
    </div>
    """, unsafe_allow_html=True)
