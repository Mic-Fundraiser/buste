import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from zipfile import ZipFile
import io

# Calcola la larghezza delle colonne laterali per centrare l'immagine
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.write("")  # Colonna vuota per spaziatura

with col2:
    st.image("http://michelangelogigli.it/wp-content/uploads/2023/06/logo-michelangelo-gigli-consulente-fundraising.png", width=200)  # Modifica 'width' a seconda delle dimensioni desiderate

with col3:
    st.write("")  # Colonna vuota per spaziatura



# Definizione delle dimensioni della pagina per un layout orizzontale
custom_page_width = 22 * cm  # Larghezza
custom_page_height = 11 * cm  # Altezza
custom_page_size = (custom_page_width, custom_page_height)

# Creazione della cartella temporanea per i PDF
output_folder = "pdf_outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Funzione modificata per creare un PDF per ogni riga del dataframe
def create_individual_pdf(row, logo_path, sender_address, output_folder):
    output_pdf_path = f"{output_folder}/{row['Cognome']}_{row['Nome']}.pdf"
    margin = 1 * cm
    logo_size = 2 * cm  # Dimensione del logo
    text_size = 10
    sender_text_y = custom_page_height - margin - logo_size / 2  # Posizione del testo del mittente vicino al logo

    c = canvas.Canvas(output_pdf_path, pagesize=custom_page_size)
    c.setFont("Helvetica", 12)

    # Disegna il logo in alto a sinistra, se presente
    if logo_path is not None:
        c.drawImage(logo_path, margin, custom_page_height - margin - logo_size, width=logo_size, height=logo_size)

    # Stampa l'indirizzo del mittente accanto al logo
    for i, line in enumerate(sender_address.split('\n')):
        c.drawString(margin + (logo_size if logo_path is not None else 0) + 5, sender_text_y - (i * 15), line)

    # Stampa l'indirizzo del destinatario
    recipient_name_x = custom_page_width - margin - 6 * cm
    recipient_name_y = margin + 2 * cm
    c.drawString(recipient_name_x, recipient_name_y, f"{row['Cognome']} {row['Nome']}")
    c.drawString(recipient_name_x, recipient_name_y - 15, row['Indirizzo'])
    c.drawString(recipient_name_x, recipient_name_y - 30, f"{row['CAP']} {row['Città']} ({row['Provincia']})")

    c.showPage()
    c.save()

# Funzione per comprimere i file in un archivio ZIP e restituire il percorso del file
def compress_files_to_zip(output_folder, zip_name):
    with ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    return zip_name

# Interfaccia utente Streamlit
st.title("Generatore di buste singole con logo, mittente e destinatario")
st.write("Usare questo tracciato di esempio in .csv: Cognome |	Nome |	Indirizzo |	CAP |	Città |	Provincia")

uploaded_csv = st.file_uploader("Carica il file CSV con i dati degli indirizzi", type='csv')
uploaded_logo = st.file_uploader("Carica il logo (opzionale)", type=['png', 'jpg', 'jpeg'])
nome_azienda = st.text_input("Nome Azienda/Associazione")
via_e_numero = st.text_input("Via e numero civico")
cap = st.text_input("CAP")
città = st.text_input("Città")
sigla_provincia = st.text_input("Sigla Provincia")

if st.button("Genera PDF"):
    if uploaded_csv is not None:
        # Gestione del caricamento del logo
        logo_path = None
        if uploaded_logo is not None:
            logo_bytes = io.BytesIO(uploaded_logo.getvalue())
            logo_path = f"{output_folder}/uploaded_logo.png"
            with open(logo_path, 'wb') as f:
                f.write(logo_bytes.read())
        
        # Lettura del CSV
        dataframe = pd.read_csv(uploaded_csv)

        # Costruzione dell'indirizzo del mittente
        sender_address = f"{nome_azienda}\n{via_e_numero}\n{cap} {città} ({sigla_provincia})"

        # Creazione dei PDF
        for index, row in dataframe.iterrows():
            create_individual_pdf(row, logo_path, sender_address, output_folder)

        # Comprimi e offri il download
        zip_name = "output_pdfs.zip"
        zip_path = compress_files_to_zip(output_folder, zip_name)
        with open(zip_path, "rb") as f:
            st.download_button("Scarica lo ZIP con le buste", f, file_name=zip_name)


# Footer
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
  <p>Made By Michelangelo Gigli</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

