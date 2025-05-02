import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della pagina
st.set_page_config(
    page_title='Dashboard Raccolto Umbria',
    page_icon='📊',
    layout='wide'
)

# Colori estratti dal logo
TEAL = '#00839E'
PINK = '#D17DA6'

# Logo da URL
logo_url = 'https://liberisubito.it/wp-content/uploads/2022/12/LogoPDL_SITO_AltoSinistra.png'
st.image(logo_url, width=300)

# Titolo principale
st.markdown(f"<h1 style='color:{TEAL};'>Visualizzazione Dati - Raccolto in Umbria</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color:{PINK};'>Liberi Subito - Libero fino alla fine</h4>", unsafe_allow_html=True)

# Dati delle province
st.subheader('Totale Raccolto per Provincia')
data = {
    'Provincia': ['Perugia', 'Terni'],
    'Totale Raccolto': [1200, 850]
}
df = pd.DataFrame(data)

# Stile della tabella
df_style = df.style.format({'Totale Raccolto': '{:,.0f}'}).hide_index()
st.dataframe(df_style, use_container_width=True)

# Calcolo totale e obiettivo
total_collected = df['Totale Raccolto'].sum()
objective = 5000
progress = total_collected / objective

# Sezione Obiettivo
st.subheader('Obiettivo Raccolto')
col1, col2, col3 = st.columns(3)
col1.metric('Totale Raccolto', f"{total_collected:,}")
col2.metric('Obiettivo Totale', f"{objective:,}")
col3.metric('Percentuale Raggiunta', f"{progress:.1%}")

# Barra di progresso
st.progress(progress)

# Grafico a barre: raccolto vs obiettivo
st.subheader('Grafico: Raccolto vs Obiettivo')
bar_df = pd.DataFrame({
    'Categoria': ['Raccolto Attuale', 'Obiettivo'],
    'Valore': [total_collected, objective]
})
fig_bar = px.bar(
    bar_df,
    x='Categoria',
    y='Valore',
    text='Valore',
    color='Categoria',
    color_discrete_map={
        'Raccolto Attuale': TEAL,
        'Obiettivo': PINK
    },
    title='Confronto tra Raccolto Attuale e Obiettivo'
)
fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
fig_bar.update_layout(showlegend=False, yaxis_title='Quantità')
st.plotly_chart(fig_bar, use_container_width=True)

# Grafico a torta: distribuzione per provincia
st.subheader('Distribuzione del Raccolto per Provincia')
fig_pie = px.pie(
    df,
    names='Provincia',
    values='Totale Raccolto',
    color_discrete_sequence=[TEAL, PINK],
    title='Percentuale Raccolto per Provincia'
)
st.plotly_chart(fig_pie, use_container_width=True)

# Footer stilizzato
st.markdown(
    f"<div style='background-color:{PINK};padding:10px;text-align:center;color:white;'>© 2025 PDL - La Legge Regionale</div>",
    unsafe_allow_html=True
)
