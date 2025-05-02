import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configurazione della pagina
st.set_page_config(
    page_title='Dashboard Raccolto Umbria',
    page_icon='📊',
    layout='wide'
)

# Definizione dei colori estratti dal logo
teal = '#00839E'
pink = '#D17DA6'

# Caricamento dinamico del logo
logo_filename = 'LogoPDL_SITO_AltoSinistra (1).png'
app_dir = os.path.dirname(__file__)
logo_path = os.path.join(app_dir, logo_filename)
if os.path.exists(logo_path):
    st.image(logo_path, use_column_width=False, width=300)
else:
    st.warning(f"Logo non trovato: {logo_path}")

# Titoli e descrizione
st.title('Visualizzazione Dati - Raccolto in Umbria')
st.markdown('**Liberi Subito** - Libero fino alla fine')

# Dati delle province
data = {
    'Provincia': ['Perugia', 'Terni'],
    'Totale Raccolto': [1200, 850]
}
df = pd.DataFrame(data)

# Mostra tabella
st.header('Tabella: Totale Raccolto per Provincia')
st.table(df)

# Grafico a torta
st.header('Grafico a Torta: Distribuzione del Raccolto')
fig = px.pie(
    df,
    names='Provincia',
    values='Totale Raccolto',
    color_discrete_sequence=[teal, pink],
    title='Percentuale Raccolto per Provincia'
)
st.plotly_chart(fig, use_container_width=True)

# Footer con stile
st.markdown(
    '<div style="background-color:'+ pink +';padding:10px;text-align:center;color:white;">'
    '© 2025 PDL - La Legge Regionale</div>',
    unsafe_allow_html=True
)
