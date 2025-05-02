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

# =====================
# Connessione a Google Sheets
# =====================
# Pubblica il tuo Google Sheet come CSV (File > Pubblica sul web)
# e copia il link CSV qui sotto
# Esempio: https://docs.google.com/spreadsheets/d/1itgXHp_mmD6HwPZK_JQLp9p3oGazEomC3RsZeN2WNgc/export?format=csv&gid=0
sheet_csv_url = 'https://docs.google.com/spreadsheets/d/1itgXHp_mmD6HwPZK_JQLp9p3oGazEomC3RsZeN2WNgc/export?format=csv&gid=0'

@st.cache_data(show_spinner=False)
def load_data(url):
    """Carica CSV da Google Sheets: prova delimitatore comma, poi punto e virgola."""
    for params in ({}, {'sep': ';', 'engine': 'python'}):
        try:
            return pd.read_csv(url, **params)
        except Exception:
            continue
    st.error('Errore nel caricamento dei dati da Google Sheets. Controlla l'URL e il formato CSV.')
    return None

# Carica dati
df = load_data(sheet_csv_url)
if df is None:
    st.stop()

# Normalizzazione colonne (trasforma in stringhe e rimuove spazi)
df.columns = [str(c).strip() for c in df.columns]

# Controllo colonne richieste
required_cols = {'Provincia', 'Totale Raccolto'}
if not required_cols.issubset(df.columns):
    st.error(f"Il dataset deve contenere le colonne: {', '.join(required_cols)}")
    st.stop()

# Conversione tipo e pulizia
df['Totale Raccolto'] = pd.to_numeric(df['Totale Raccolto'], errors='coerce').fillna(0)

# =====================
# Visualizzazioni
# =====================
# Tabella dati
st.subheader('Totale Raccolto per Provincia')
df_display = df.copy()
df_display['Totale Raccolto'] = df_display['Totale Raccolto'].map('{:,.0f}'.format)
st.table(df_display)

# Calcolo totale e obiettivo
total_collected = df['Totale Raccolto'].sum()
objective = 5000
progress = total_collected / objective if objective > 0 else 0

# Sezione Obiettivo
st.subheader('Obiettivo Raccolto')
col1, col2, col3 = st.columns(3)
col1.metric('Totale Raccolto', f"{total_collected:,}")
col2.metric('Obiettivo Totale', f"{objective:,}")
col3.metric('Percentuale Raggiunta', f"{progress:.1%}")
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

# Footer
st.markdown(
    f"<div style='background-color:{PINK};padding:10px;text-align:center;color:white;'>© 2025 PDL - La Legge Regionale</div>",
    unsafe_allow_html=True
)
