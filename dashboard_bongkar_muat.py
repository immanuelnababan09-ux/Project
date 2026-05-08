import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Logistics Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0f;
    color: #e8dcc8;
}

.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1400px;
}

/* ── Remove default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Page header ── */
.page-header {
    text-align: center;
    padding: 3rem 0 2.5rem;
    border-bottom: 1px solid rgba(212,175,55,0.25);
    margin-bottom: 2.5rem;
}
.page-header h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    letter-spacing: 0.08em;
    color: #f0e6c8;
    margin: 0;
}
.page-header p {
    font-size: 0.8rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c9a84c;
    margin: 0.5rem 0 0;
}

/* ── Section label ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 0.4rem;
    display: block;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: #f0e6c8;
    margin: 0 0 1.2rem;
}

/* ── Card container ── */
.card-container {
    background: linear-gradient(135deg, #1a1a1b 0%, #161617 100%);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 4px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.card-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #c9a84c, #7a6230);
}

/* ── KPI / metric cards ── */
.kpi-wrap {
    background: linear-gradient(135deg, #1e1c17 0%, #181714 100%);
    border: 1px solid rgba(212,175,55,0.28);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    position: relative;
}
.kpi-wrap::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%; transform: translateX(-50%);
    width: 60%; height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
}
.kpi-label {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #9a8a6a;
    display: block;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: #d4af37;
    line-height: 1;
}
.kpi-unit {
    font-size: 0.7rem;
    color: #9a8a6a;
    display: block;
    margin-top: 0.3rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent);
    margin: 2.5rem 0;
    border: none;
}

/* ── Filter label ── */
.stMultiSelect label, .stSelectbox label {
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #9a8a6a !important;
}

/* ── Plotly chart area background ── */
.js-plotly-plot { border-radius: 3px; }

/* ── Info box ── */
.info-box {
    background: rgba(201,168,76,0.07);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 3px;
    padding: 0.8rem 1.1rem;
    font-size: 0.8rem;
    color: #b89d60;
    letter-spacing: 0.04em;
    margin-top: 0.8rem;
}

/* ── Table ── */
.stDataFrame {
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 4px !important;
}

/* ── Streamlit metric override ── */
[data-testid="metric-container"] {
    background: transparent !important;
}

/* ── Input widgets ── */
.stMultiSelect > div > div {
    background: #1a1a1b !important;
    border-color: rgba(212,175,55,0.25) !important;
}
.stSelectbox > div > div {
    background: #1a1a1b !important;
    border-color: rgba(212,175,55,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY TEMPLATE ─────────────────────────────────────────────────────────
GOLD_PALETTE = ["#d4af37", "#c9a84c", "#b08d30", "#8c6e24", "#f0d060", "#e8c450", "#a07820"]
DARK_BG     = "#111112"
CARD_BG     = "#161617"
GRID_COLOR  = "rgba(212,175,55,0.08)"
TEXT_COLOR  = "#c8b890"

def dark_layout(title="", height=360):
    return dict(
        height=height,
        title=dict(text=title, font=dict(family="Cormorant Garamond, serif", size=16, color="#d4af37"), x=0.01),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=TEXT_COLOR, size=11),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor="rgba(201,168,76,0.15)", tickcolor="transparent", zeroline=False),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor="rgba(201,168,76,0.15)", tickcolor="transparent", zeroline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
        margin=dict(l=20, r=20, t=48, b=20),
        colorway=GOLD_PALETTE,
    )

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    file_path = 'BONGKAR_2.xlsx'
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names
    t_b = next((s for s in sheets if 'bongkar' in s.lower()), None)
    t_m = next((s for s in sheets if 'muat'   in s.lower()), None)
    if not t_b or not t_m:
        raise ValueError(f"Sheet tidak lengkap! Ditemukan: {sheets}")
    df_b = pd.read_excel(file_path, sheet_name=t_b); df_b['Aktivitas'] = 'Bongkar'
    df_m = pd.read_excel(file_path, sheet_name=t_m); df_m['Aktivitas'] = 'Muat'
    df   = pd.concat([df_b, df_m], ignore_index=True)
    df['Berat'] = pd.to_numeric(df['Berat'], errors='coerce').fillna(0)
    return df

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>Logistics Intelligence Dashboard</h1>
    <p>Analisis Arus Bongkar &amp; Muat — Data Hub Regional</p>
</div>
""", unsafe_allow_html=True)

# ─── MAIN ────────────────────────────────────────────────────────────────────
try:
    df = load_data()

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 1 — KPI SCORECARD
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Ringkasan Kinerja</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Indikator Utama</p>', unsafe_allow_html=True)

    vol_b      = df[df['Aktivitas'] == 'Bongkar']['Berat'].sum()
    vol_m      = df[df['Aktivitas'] == 'Muat'   ]['Berat'].sum()
    throughput = vol_b + vol_m
    ratio      = (vol_b / vol_m) if vol_m else 0
    n_komo     = df['Komoditas'].nunique()

    k1, k2, k3, k4, k5 = st.columns(5)
    def kpi(col, label, value, unit):
        col.markdown(f"""
        <div class="kpi-wrap">
            <span class="kpi-label">{label}</span>
            <div class="kpi-value">{value}</div>
            <span class="kpi-unit">{unit}</span>
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Total Bongkar",    f"{vol_b:,.0f}",      "Ton")
    kpi(k2, "Total Muat",       f"{vol_m:,.0f}",      "Ton")
    kpi(k3, "Total Throughput", f"{throughput:,.0f}", "Ton")
    kpi(k4, "Rasio B/M",        f"{ratio:.2f}",        "Bongkar per Muat")
    kpi(k5, "Jenis Komoditas",  f"{n_komo}",           "Komoditas")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 2 — KOMPOSISI + TOP 5
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Komposisi & Peringkat</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Distribusi Aktivitas</p>', unsafe_allow_html=True)

    col_pie, col_top_b, col_top_m = st.columns([1, 1.4, 1.4])

    with col_pie:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Bongkar', 'Muat'],
            values=[vol_b, vol_m],
            hole=0.62,
            marker=dict(colors=["#d4af37", "#4a3a1a"],
                        line=dict(color="#111112", width=2)),
            textinfo='percent',
            textfont=dict(color="#e8dcc8", size=12),
            insidetextorientation='horizontal',
        ))
        fig_pie.add_annotation(
            text=f"<b>{throughput:,.0f}</b><br><span style='font-size:9px'>Total Ton</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Cormorant Garamond, serif", size=14, color="#d4af37"),
            align="center"
        )
        fig_pie.update_layout(**dark_layout("Komposisi Aktivitas", height=280))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_top_b:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        top5_b = (df[df['Aktivitas'] == 'Bongkar']
                  .groupby('Komoditas')['Berat'].sum()
                  .nlargest(5).reset_index()
                  .sort_values('Berat'))
        fig_b = go.Figure(go.Bar(
            x=top5_b['Berat'], y=top5_b['Komoditas'],
            orientation='h',
            marker=dict(
                color=top5_b['Berat'],
                colorscale=[[0,"#4a3518"],[0.5,"#b08d30"],[1,"#f0d060"]],
                line=dict(width=0)
            ),
            text=[f"{v:,.0f}" for v in top5_b['Berat']],
            textposition='outside',
            textfont=dict(color="#c8b890", size=10),
        ))
        fig_b.update_layout(**dark_layout("Top 5 Komoditas Bongkar", height=280))
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_top_m:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        top5_m = (df[df['Aktivitas'] == 'Muat']
                  .groupby('Komoditas')['Berat'].sum()
                  .nlargest(5).reset_index()
                  .sort_values('Berat'))
        fig_m = go.Figure(go.Bar(
            x=top5_m['Berat'], y=top5_m['Komoditas'],
            orientation='h',
            marker=dict(
                color=top5_m['Berat'],
                colorscale=[[0,"#1a2a3a"],[0.5,"#3a6a8a"],[1,"#70b0d0"]],
                line=dict(width=0)
            ),
            text=[f"{v:,.0f}" for v in top5_m['Berat']],
            textposition='outside',
            textfont=dict(color="#c8b890", size=10),
        ))
        fig_m.update_layout(**dark_layout("Top 5 Komoditas Muat", height=280))
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 3 — TREN MUSIMAN
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Analisis Temporal</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Tren & Musiman Bulanan</p>', unsafe_allow_html=True)

    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    df_time = df.groupby(['Bulan','Aktivitas'])['Berat'].sum().reset_index()

    fig_line = go.Figure()
    for act, color in [('Bongkar','#d4af37'), ('Muat','#5a8fa8')]:
        d = df_time[df_time['Aktivitas'] == act]
        fig_line.add_trace(go.Scatter(
            x=d['Bulan'], y=d['Berat'], mode='lines+markers', name=act,
            line=dict(color=color, width=2.5),
            marker=dict(size=7, color=color, line=dict(color="#111112", width=1.5)),
            fill='tozeroy',
            fillcolor=color.replace('#','rgba(').replace('d4af37','212,175,55,0.06)').replace('5a8fa8','90,143,168,0.04)'),
        ))
    fig_line.update_layout(**dark_layout("Perbandingan Volume Bulanan — Bongkar vs Muat", height=320))
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('<div class="info-box">Grafik ini membantu pimpinan memprediksi kapan pelabuhan akan sangat sibuk (Peak Season) dan merencanakan alokasi sumber daya secara optimal.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 4 — ANALISIS UTAMA (filter + tren + bar)
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Analisis Terfilter</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Arus Barang per Komoditas</p>', unsafe_allow_html=True)

    all_komo = df['Komoditas'].unique().tolist()
    sel_komo = st.multiselect(
        "Pilih Komoditas:",
        all_komo, default=all_komo[:3]
    )
    df_f = df[df['Komoditas'].isin(sel_komo)] if sel_komo else df

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        pivot_line = df_f.pivot_table(index='Bulan', columns='Aktivitas', values='Berat', aggfunc='sum').reset_index()
        fig_fl = go.Figure()
        for act, color in [('Bongkar','#d4af37'), ('Muat','#5a8fa8')]:
            if act in pivot_line.columns:
                fig_fl.add_trace(go.Scatter(
                    x=pivot_line['Bulan'], y=pivot_line[act],
                    mode='lines+markers', name=act,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6, color=color),
                ))
        fig_fl.update_layout(**dark_layout("Tren Berat per Bulan", height=300))
        st.plotly_chart(fig_fl, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        bar_data = df_f.groupby(['Komoditas','Aktivitas'])['Berat'].sum().reset_index()
        fig_bar = px.bar(
            bar_data, x='Komoditas', y='Berat', color='Aktivitas',
            barmode='group',
            color_discrete_map={'Bongkar':'#d4af37','Muat':'#5a8fa8'},
        )
        fig_bar.update_layout(**dark_layout("Perbandingan Volume per Komoditas", height=300))
        fig_bar.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<span class="section-label" style="margin-bottom:0.8rem;display:block">Tabel Data Terfilter</span>', unsafe_allow_html=True)
    st.dataframe(
        df_f.style.set_properties(**{
            'background-color': '#161617',
            'color': '#c8b890',
            'border-color': 'rgba(212,175,55,0.15)',
        }),
        use_container_width=True, height=260
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 5 — ANALISIS KOMODITAS SPESIFIK
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Deep Dive</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Analisis Komoditas Unggulan</p>', unsafe_allow_html=True)

    komo_pilihan = st.selectbox("Pilih Komoditas Spesifik:", df['Komoditas'].unique())
    df_spesifik  = df[df['Komoditas'] == komo_pilihan]

    col_area, col_pareto = st.columns([1.2, 1])

    with col_area:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        fig_area = go.Figure()
        for act, color, fill_c in [
            ('Bongkar','#d4af37','rgba(212,175,55,0.12)'),
            ('Muat',   '#5a8fa8','rgba(90,143,168,0.08)')
        ]:
            d = df_spesifik[df_spesifik['Aktivitas'] == act]
            fig_area.add_trace(go.Scatter(
                x=d['Bulan'], y=d['Berat'], name=act,
                mode='lines', fill='tozeroy',
                line=dict(color=color, width=2),
                fillcolor=fill_c,
            ))
        fig_area.update_layout(**dark_layout(f"Volume Bulanan — {komo_pilihan}", height=300))
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pareto:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        pareto = (df.groupby('Komoditas')['Berat'].sum()
                  .sort_values(ascending=False).reset_index())
        pareto['Kumulatif %'] = pareto['Berat'].cumsum() / pareto['Berat'].sum() * 100

        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=pareto['Komoditas'], y=pareto['Berat'], name='Volume',
            marker=dict(
                color=pareto['Berat'],
                colorscale=[[0,"#3a2800"],[0.5,"#b08d30"],[1,"#f0d060"]],
                line=dict(width=0)
            ),
        ))
        fig_pareto.add_trace(go.Scatter(
            x=pareto['Komoditas'], y=pareto['Kumulatif %'],
            name='Kumulatif %', yaxis='y2',
            mode='lines+markers',
            line=dict(color='#c06050', width=2, dash='dot'),
            marker=dict(size=5),
        ))
        layout = dark_layout("Kategorisasi Pareto Komoditas", height=300)
        layout['yaxis2'] = dict(
            overlaying='y', side='right',
            gridcolor="rgba(0,0,0,0)",
            range=[0, 110],
            ticksuffix='%', tickcolor='transparent',
            tickfont=dict(color=TEXT_COLOR)
        )
        layout['legend'] = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR), x=0.02, y=0.98)
        fig_pareto.update_layout(**layout)
        st.plotly_chart(fig_pareto, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 6 — KESEIMBANGAN PERDAGANGAN
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<span class="section-label">Neraca Regional</span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Keseimbangan Perdagangan</p>', unsafe_allow_html=True)

    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    df_pv = df.pivot_table(index='Komoditas', columns='Aktivitas', values='Berat', aggfunc='sum').fillna(0)
    df_pv['Gap'] = df_pv.get('Bongkar', 0) - df_pv.get('Muat', 0)
    df_gap = df_pv.reset_index().sort_values('Gap')

    colors_gap = ['#5a8fa8' if g < 0 else '#d4af37' for g in df_gap['Gap']]
    fig_gap = go.Figure(go.Bar(
        x=df_gap['Komoditas'], y=df_gap['Gap'],
        marker=dict(color=colors_gap, line=dict(width=0)),
        text=[f"{v:,.0f}" for v in df_gap['Gap']],
        textposition='outside',
        textfont=dict(color="#c8b890", size=10),
    ))
    fig_gap.add_hline(y=0, line_color="rgba(212,175,55,0.35)", line_width=1)
    fig_gap.update_layout(**dark_layout("Analisis Gap — Bongkar vs Muat per Komoditas", height=340))
    st.plotly_chart(fig_gap, use_container_width=True)

    st.markdown("""
    <div class="info-box">
        Batang <span style="color:#d4af37;font-weight:600">kuning (positif)</span> menandakan komoditas dengan dominasi Bongkar — lebih banyak barang masuk (konsumsi tinggi).
        Batang <span style="color:#5a8fa8;font-weight:600">biru (negatif)</span> menandakan dominasi Muat — lebih banyak barang keluar (produksi/ekspor lokal).
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid rgba(212,175,55,0.1);margin-top:2rem">
        <p style="font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;color:rgba(201,168,76,0.4)">
            Logistics Intelligence Dashboard — Data Bongkar Muat Regional
        </p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.markdown(f"""
    <div class="card-container" style="border-color:rgba(180,60,60,0.4)">
        <span class="section-label" style="color:#c05050">Error</span>
        <p style="color:#e8a0a0">Terjadi kendala memuat data: <code>{e}</code></p>
        <p style="color:#9a8a6a;font-size:0.8rem">Pastikan file <code>BONGKAR_2.xlsx</code> berada di direktori yang sama dengan script ini.</p>
    </div>
    """, unsafe_allow_html=True)
