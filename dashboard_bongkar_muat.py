import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Logistics Intelligence Dashboard", layout="wide")

# --- FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    file_path = 'BONGKAR_2.xlsx'
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    # Mencari sheet bongkar dan muat secara otomatis
    t_bongkar = next((s for s in sheet_names if 'bongkar' in s.lower()), None)
    t_muat = next((s for s in sheet_names if 'muat' in s.lower()), None)
    
    if not t_bongkar or not t_muat:
        raise ValueError(f"Sheet tidak lengkap! Ditemukan: {sheet_names}")
    
    df_b = pd.read_excel(file_path, sheet_name=t_bongkar)
    df_b['Aktivitas'] = 'Bongkar'
    
    df_m = pd.read_excel(file_path, sheet_name=t_muat)
    df_m['Aktivitas'] = 'Muat'
    
    df_total = pd.concat([df_b, df_m], ignore_index=True)
    df_total['Berat'] = pd.to_numeric(df_total['Berat'], errors='coerce').fillna(0)
    
    return df_total

# --- TAMPILAN UTAMA ---
st.title("🚢 Logistics Data Hub: Analisis Bongkar Muat")

try:
    df = load_data()

    # MEMBUAT 5 TAB
    tab_awal, tab_exec, tab_tren, tab_komoditas, tab_trade = st.tabs([
        "🏠 Analisis Utama", 
        "📊 Ringkasan Eksekutif", 
        "📈 Tren & Musiman", 
        "📦 Komoditas Unggulan", 
        "⚖️ Keseimbangan Perdagangan"
    ])

    # --- TAB 1: ANALISIS UTAMA (KODE AWAL) ---
    with tab_awal:
        st.header("Analisis Dasar Arus Barang")
        all_komo = df['Komoditas'].unique().tolist()
        sel_komo = st.multiselect("Filter Komoditas (Tab Utama):", all_komo, default=all_komo[:3], key="main_komo")
        
        df_f = df[df['Komoditas'].isin(sel_komo)]
        
        st.subheader("Tren Berat Per Bulan")
        st.line_chart(df_f.pivot_table(index='Bulan', columns='Aktivitas', values='Berat', aggfunc='sum'))
        
        st.subheader("Perbandingan Volume")
        st.bar_chart(df_f.groupby(['Komoditas', 'Aktivitas'])['Berat'].sum().unstack())

        st.subheader("📄 Tabel Data Terfilter")
        st.dataframe(df_f, use_container_width=True)

    # --- TAB 2: EXECUTIVE SUMMARY ---
    with tab_exec:
        st.header("Dashboard Ringkasan Kinerja")
        
        vol_b = df[df['Aktivitas'] == 'Bongkar']['Berat'].sum()
        vol_m = df[df['Aktivitas'] == 'Muat']['Berat'].sum()
        throughput = vol_b + vol_m
        
        # Metrik Kartu (Scorecard)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Bongkar", f"{vol_b:,.0f} Ton")
        c2.metric("Total Muat", f"{vol_m:,.0f} Ton")
        c3.metric("Total Throughput", f"{throughput:,.0f} Ton")
        
        col_pie, col_top = st.columns(2)
        with col_pie:
            st.subheader("Komposisi Aktivitas")
            fig_pie = px.pie(df, values='Berat', names='Aktivitas', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_top:
            st.subheader("Top 5 Komoditas Terbesar")
            top5 = df.groupby('Komoditas')['Berat'].sum().nlargest(5).reset_index()
            fig_top = px.bar(top5, x='Berat', y='Komoditas', orientation='h', color='Komoditas')
            st.plotly_chart(fig_top, use_container_width=True)

    # --- TAB 3: TREN & MUSIMAN ---
    with tab_tren:
        st.header("Analisis Tren dan Musiman")
        df_time = df.groupby(['Bulan', 'Aktivitas'])['Berat'].sum().reset_index()
        fig_time = px.line(df_time, x='Bulan', y='Berat', color='Aktivitas', markers=True, title="Perbandingan Musiman Bongkar vs Muat")
        st.plotly_chart(fig_time, use_container_width=True)
        st.info("💡 Grafik ini membantu pimpinan memprediksi kapan pelabuhan akan sangat sibuk (Peak Season).")

    # --- TAB 4: ANALISIS KOMODITAS ---
    with tab_komoditas:
        st.header("Analisis Komoditas Unggulan")
        # Detail Filter Per Komoditas tunggal
        komo_pilihan = st.selectbox("Pilih Komoditas Spesifik:", df['Komoditas'].unique())
        df_spesifik = df[df['Komoditas'] == komo_pilihan]
        
        st.subheader(f"Statistik Detail: {komo_pilihan}")
        fig_area = px.area(df_spesifik, x='Bulan', y='Berat', color='Aktivitas', template="plotly_dark")
        st.plotly_chart(fig_area, use_container_width=True)
        
        st.subheader("Kategorisasi Barang (Pareto)")
        pareto_data = df.groupby('Komoditas')['Berat'].sum().sort_values(ascending=False).reset_index()
        st.bar_chart(pareto_data.set_index('Komoditas'))

    # --- TAB 5: KESEIMBANGAN PERDAGANGAN ---
    with tab_trade:
        st.header("Keseimbangan Perdagangan Regional")
        # Pivot untuk menghitung selisih
        df_pv = df.pivot_table(index='Komoditas', columns='Aktivitas', values='Berat', aggfunc='sum').fillna(0)
        df_pv['Gap (B-M)'] = df_pv['Bongkar'] - df_pv['Muat']
        
        st.subheader("Analisis Gap (Masuk vs Keluar)")
        fig_gap = px.bar(df_pv.reset_index(), x='Komoditas', y='Gap (B-M)', 
                         color='Gap (B-M)', color_continuous_scale='Picnic')
        st.plotly_chart(fig_gap, use_container_width=True)
        st.write("Catatan: Angka **Positif** berarti lebih banyak barang masuk (konsumsi), **Negatif** berarti lebih banyak keluar (produksi).")

except Exception as e:
    st.error(f"Terjadi kendala: {e}")