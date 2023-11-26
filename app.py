import streamlit as st
import pandas as pd
import altair as alt
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Analisis Data Ekspor-Impor Indonesia",
    # page_icon="https://www.bps.go.id/images/bps.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

selected = option_menu(
    None,
    ['Home', 'Analysis'],
    icons=['house', 'graph-up'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0px!important", "background-color": "#fafafa", "font-family": "arial",
                      "letter-spacing": "0.5px"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "padding": "10px", "margin": "0px",
                     "--hover-color": "#eee", "color": "#2b2b2b"},
        "nav-link-selected": {"background-color": "#E3476C"},
    }
)

st.markdown("<h1 style='text-align: center;'>Data Ekspor-Impor Indonesia</h1>", unsafe_allow_html=True)
st.markdown(
    "<h6 style='text-align: center; color: grey;'>Data Source: Badan Pusat Statistik <a href='https://www.bps.go.id/exim/' target='_blank'>(https://www.bps.go.id/exim/)</a></h6>",
    unsafe_allow_html=True)

"\n\n"

data_df = pd.read_csv('Data_Ekspor_Impor_Indonesia_BPS.csv')

if selected == 'Home':
    st.header('Abstrak')
    st.markdown("""
    <p style='text-align: justify;'>
        Ekspor maupun impor merupakan faktor penting dalam merangsang pertumbuhan 
ekonomi suatu negara. Ekspor dan impor akan memperbesar kapasitas konsumsi 
suatu negara, meningkatkan output dunia serta menyajikan akses ke sumber-sumber daya yang langka dan pasar-pasar internasional yang potensial untuk 
berbagai produk ekspor yang mana tanpa produk-produk tersebut maka negara-negara miskin tidak akan mampu mengembangkan kegiatan dan kehidupan 
perekonomian nasionalnya.
    </p>
""", unsafe_allow_html=True)

    st.header('Tabel Ekspor-Impor Indonesia (2014 - 2023)')
    sorted_df = data_df.copy()
    ascending = True
    sorted_df = sorted_df.sort_values('Bulan', ascending=ascending).reset_index(drop=True)
    sorted_df['Bulan'] = pd.to_datetime(sorted_df['Bulan']).dt.strftime('%B %Y')
    st.dataframe(sorted_df, use_container_width=True)

    st.header('Grafik Ekspor-Impor Indonesia (2014 - 2023)')
    chart_data = data_df.groupby('Bulan').agg({
        'Nilai Ekspor (US $)': 'sum',
        'Nilai Impor (US $)': 'sum',
        'Berat Ekspor (KG)': 'sum',
        'Berat Impor (KG)': 'sum'
    }).reset_index()
    chart_data['Tahun'] = pd.to_datetime(chart_data['Bulan']).dt.year
    chart = alt.Chart(chart_data).mark_area().encode(
        x=alt.X('Bulan:T', title=''),
        y=alt.Y('value:Q', title='', axis=alt.Axis(format=',.2f')),
        color=alt.Color('variable:N', title='Keterangan')
    ).transform_fold(
        ['Nilai Ekspor (US $)', 'Nilai Impor (US $)', 'Berat Ekspor (KG)', 'Berat Impor (KG)'],
        as_=['variable', 'value']
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    


elif selected == 'Analysis':

    # PERKEMBANGAN EKSPOR-IMPOR
    st.header('Perkembangan Ekspor-Impor Dalam Beberapa Tahun Terakhir') # st.markdown(f'<h3 style="text-align: left"> Data Ekspor & Impor Indonesia per Tahun </h3>', unsafe_allow_html=True)
    data_df['Bulan'] = pd.to_datetime(data_df['Bulan'])
    selected_years = st.slider(
        'Rentang Tahun', 
        int(data_df['Bulan'].dt.year.min()), 
        int(data_df['Bulan'].dt.year.max()), 
        (int(data_df['Bulan'].dt.year.min()), int(data_df['Bulan'].dt.year.max())))
    yearly_data = data_df[(data_df['Bulan'].dt.year >= selected_years[0]) & (data_df['Bulan'].dt.year <= selected_years[1])].groupby(data_df['Bulan'].dt.year).agg({
        'Nilai Ekspor (US $)': 'sum',
        'Nilai Impor (US $)': 'sum',
        'Berat Ekspor (KG)': 'sum',
        'Berat Impor (KG)': 'sum'
    }).reset_index()
    yearly_data = yearly_data.rename(columns={'Bulan': 'Tahun'})
    yearly_data['Tahun'] = yearly_data['Tahun'].astype(str)
    yearly_data['Keterangan'] = yearly_data.apply(lambda row: 
        'Nilai Ekspor' if pd.notna(row['Nilai Ekspor (US $)']) and pd.isna(row['Berat Ekspor (KG)']) else
        'Berat Ekspor' if pd.isna(row['Nilai Ekspor (US $)']) and pd.notna(row['Berat Ekspor (KG)']) else
        'Nilai Impor' if pd.notna(row['Nilai Impor (US $)']) and pd.isna(row['Berat Impor (KG)']) else
        'Berat Impor' if pd.isna(row['Nilai Impor (US $)']) and pd.notna(row['Berat Impor (KG)']) else None,
        axis=1
    )
    col1, col2 = st.columns(2)
    with col1:
        total_nilai_ekspor = yearly_data['Nilai Ekspor (US $)'].sum()
        st.metric("Total Nilai Ekspor (US $)", value=f"{total_nilai_ekspor:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", "."))
        total_nilai_impor = yearly_data['Nilai Impor (US $)'].sum()
        st.metric("Total Nilai Impor (US $)", value=f"{total_nilai_impor:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", "."))
    with col2:
        total_berat_ekspor = yearly_data['Berat Ekspor (KG)'].sum()
        st.metric("Total Berat Ekspor (Kg)", value=f"{total_berat_ekspor:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", "."))
        total_berat_impor = yearly_data['Berat Impor (KG)'].sum()
        st.metric("Total Berat Impor (Kg)", value=f"{total_berat_impor:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")) # st.metric("Total Berat Impor (Kg)", value=f"{total_nilai_impor:,.2f}")
    line_chart = alt.Chart(yearly_data).mark_line().encode(
        x=alt.X('Tahun', title='Tahun (Year)'),
        y=alt.Y('value:Q', title='Nilai (US $)'),
        color=alt.Color('Keterangan:N', 
                   legend=alt.Legend(title='Keterangan'),
                   scale=alt.Scale(domain=['Nilai Ekspor (US $)', 'Nilai Impor (US $)'],
                                   range=['gold', 'lightgreen'])
                  ),
        tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', format='$,.2f')]
    ).transform_fold(
        ['Nilai Ekspor (US $)', 'Nilai Impor (US $)'], as_=['Keterangan', 'value']
    ).properties(
        title='',
    )
    dots = alt.Chart(yearly_data).mark_circle(size=100, opacity=1).encode(
        x='Tahun',
        y='value:Q',
        color=alt.Color('Keterangan:N', 
                   legend=alt.Legend(title='Keterangan'),
                   scale=alt.Scale(domain=['Nilai Ekspor (US $)', 'Nilai Impor (US $)'],
                                   range=['gold', 'lightgreen'])
                  ),
        tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', format=',.2f')]
    ).transform_fold(
        ['Nilai Ekspor (US $)', 'Nilai Impor (US $)'], as_=['Keterangan', 'value']
    )
    line_chart += dots
    line_chart_berat = alt.Chart(yearly_data).mark_line().encode(
        x=alt.X('Tahun', title='Tahun (Year)'),
        y=alt.Y('value:Q', title='Berat (Kg)'),
        color=alt.Color('Keterangan:N', legend=alt.Legend(title='Keterangan')),
        tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', format=',.2f')]
    ).transform_fold(
        ['Berat Ekspor (KG)', 'Berat Impor (KG)'], as_=['Keterangan', 'value']
    ).properties(
        title='',
    )
    dots = alt.Chart(yearly_data).mark_circle(size=100, opacity=1).encode(
        x='Tahun',
        y='value:Q',
        color='Keterangan:N',
        tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', format=',.2f')]
    ).transform_fold(
        ['Berat Ekspor (KG)', 'Berat Impor (KG)'], as_=['Keterangan', 'value']
    )
    line_chart_berat += dots
    col1, col2 = st.columns(2)
    col1.altair_chart(line_chart, use_container_width=True)
    col2.altair_chart(line_chart_berat, use_container_width=True)

    # ANALISIS PERTUMBUHAN (%) EKSPOR-IMPOR
    st.header('Pertumbuhan Ekspor-Impor Indonesia Dalam Beberapa Tahun Terakhir')
    data_df['Bulan'] = pd.to_datetime(data_df['Bulan'])
    selected_years_pertumbuhan = st.slider(
    'Rentang Tahun', 
    int(data_df['Bulan'].dt.year.min()), 
    int(data_df['Bulan'].dt.year.max()), 
    (int(data_df['Bulan'].dt.year.min()), int(data_df['Bulan'].dt.year.max())),
    key="pertumbuhan_slider" 
    )
    yearly_data_pertumbuhan = data_df[(data_df['Bulan'].dt.year >= selected_years_pertumbuhan[0]) & (data_df['Bulan'].dt.year <= selected_years_pertumbuhan[1])].groupby(data_df['Bulan'].dt.year).agg({
        'Nilai Ekspor (US $)': 'sum',
        'Nilai Impor (US $)': 'sum',
        'Berat Ekspor (KG)': 'sum',
        'Berat Impor (KG)': 'sum'
    }).reset_index()
    yearly_data_pertumbuhan = yearly_data_pertumbuhan.rename(columns={'Bulan': 'Tahun'})
    yearly_data_pertumbuhan['Tahun'] = yearly_data_pertumbuhan['Tahun'].astype(str)
    yearly_data_pertumbuhan['Nilai Ekspor (%)'] = yearly_data_pertumbuhan['Nilai Ekspor (US $)'].pct_change() * 100
    yearly_data_pertumbuhan['Nilai Impor (%)'] = yearly_data_pertumbuhan['Nilai Impor (US $)'].pct_change() * 100
    yearly_data_pertumbuhan['Berat Ekspor (%)'] = yearly_data_pertumbuhan['Berat Ekspor (KG)'].pct_change() * 100
    yearly_data_pertumbuhan['Berat Impor (%)'] = yearly_data_pertumbuhan['Berat Impor (KG)'].pct_change() * 100
    yearly_data_pertumbuhan['Keterangan'] = 'Nilai Ekspor (%)'
    yearly_data_pertumbuhan['Keterangan'] = 'Nilai Impor (%)'
    yearly_data_pertumbuhan['Keterangan'] = 'Berat Ekspor (%)'
    yearly_data_pertumbuhan['Keterangan'] = 'Berat Impor (%)'

    col1, col2 = st.columns(2)
    with col1:        
        total_pertumbuhan = yearly_data_pertumbuhan['Nilai Ekspor (%)'].mean()
        st.metric("Rata-rata (Nilai Ekspor)", value=f"{total_pertumbuhan:,.2f} %".replace(",", "temp").replace(".", ",").replace("temp", "."))
        total_pertumbuhan = yearly_data_pertumbuhan['Nilai Impor (%)'].mean()
        st.metric("Rata-rata (Nilai Impor)", value=f"{total_pertumbuhan:,.2f} %".replace(",", "temp").replace(".", ",").replace("temp", "."))
    with col2:
        total_pertumbuhan = yearly_data_pertumbuhan['Berat Ekspor (%)'].mean()
        st.metric("Rata-rata (Berat Ekspor)", value=f"{total_pertumbuhan:,.2f} %".replace(",", "temp").replace(".", ",").replace("temp", "."))     
        total_pertumbuhan = yearly_data_pertumbuhan['Berat Impor (%)'].mean()
        st.metric("Rata-rata (Berat Impor)", value=f"{total_pertumbuhan:,.2f} %".replace(",", "temp").replace(".", ",").replace("temp", "."))
        
    pertumbuhan_chart = alt.Chart(yearly_data_pertumbuhan).mark_line().encode(
    x=alt.X('Tahun', title='Tahun (Year)'),
    y=alt.Y('value:Q', title='Pertumbuhan (%)'),
    color=alt.Color('Keterangan:N', legend=alt.Legend(title='Keterangan')),
    tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', title='Pertumbuhan (%)', format=',.2f', formatType='number')]
    ).transform_fold(
        ['Nilai Ekspor (%)', 'Nilai Impor (%)', 'Berat Ekspor (%)', 'Berat Impor (%)'], as_=['Keterangan', 'value']
    ).properties(
        title='',
    )
    dots = alt.Chart(yearly_data_pertumbuhan).mark_circle(size=100, opacity=1).encode(
    x=alt.X('Tahun', title='Tahun (Year)'),
    y=alt.Y('value:Q', title='Pertumbuhan (%)'),
    color=alt.Color('Keterangan:N', legend=alt.Legend(title='Keterangan')),
    tooltip=['Keterangan', 'Tahun', alt.Tooltip('value:Q', title='Pertumbuhan (%)', format=',.2f', formatType='number')]
    ).transform_fold(
        ['Nilai Ekspor (%)', 'Nilai Impor (%)', 'Berat Ekspor (%)', 'Berat Impor (%)'], as_=['Keterangan', 'value']
    )
    pertumbuhan_chart += dots
    st.altair_chart(pertumbuhan_chart, use_container_width=True)

    # NERACA PERDAGANGAN
    st.header('Neraca Perdagangan')
    data_df['Bulan'] = pd.to_datetime(data_df['Bulan'])
    selected_years_neraca = st.slider(
    'Rentang Tahun', 
    int(data_df['Bulan'].dt.year.min()), 
    int(data_df['Bulan'].dt.year.max()), 
    (int(data_df['Bulan'].dt.year.min()), int(data_df['Bulan'].dt.year.max())),
    key="neraca_slider" 
    )
    yearly_data_neraca = data_df[(data_df['Bulan'].dt.year >= selected_years_neraca[0]) & (data_df['Bulan'].dt.year <= selected_years_neraca[1])].groupby(data_df['Bulan'].dt.year).agg({
        'Nilai Ekspor (US $)': 'sum',
        'Nilai Impor (US $)': 'sum'
    }).reset_index()
    yearly_data_neraca = yearly_data_neraca.rename(columns={'Bulan': 'Tahun'})
    yearly_data_neraca['Tahun'] = yearly_data_neraca['Tahun'].astype(str)
    yearly_data_neraca['Neraca Perdagangan (US $)'] = yearly_data_neraca['Nilai Ekspor (US $)'] - yearly_data_neraca['Nilai Impor (US $)']
    col1, col2 = st.columns(2)
    with col1:
        total_neraca_perdagangan = yearly_data_neraca['Neraca Perdagangan (US $)'].sum()
        st.metric("Total Neraca Perdagangan (US $)", value=f"{total_neraca_perdagangan:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", "."))
    with col2:
        rata_rata_neraca_perdagangan = yearly_data_neraca['Neraca Perdagangan (US $)'].mean()
        st.metric("Rata-rata Neraca Perdagangan (US $)", value=f"{rata_rata_neraca_perdagangan:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", "."))
    
    yearly_data_neraca['Keterangan'] = yearly_data_neraca['Neraca Perdagangan (US $)'].apply(lambda x: 'Surplus' if x >= 0 else 'Defisit')
    bar_chart_neraca = alt.Chart(yearly_data_neraca).mark_bar().encode(
        x=alt.X('Tahun:N', title='Tahun (Year)'),
        y=alt.Y('Neraca Perdagangan (US $):Q', title='Nilai (US $)'),
        color=alt.Color('Keterangan:N', scale=alt.Scale(domain=['Surplus', 'Defisit'], range=['lawngreen', 'orangered'])), 
        tooltip=['Tahun', alt.Tooltip('Neraca Perdagangan (US $):Q', format=',.2f'), 'Keterangan']
    ).properties(
        title='',
    )
    st.altair_chart(bar_chart_neraca, use_container_width=True)
