import streamlit as st
import wikipedia
import random

# Asetukset
st.set_page_config(page_title="Sukututkijan Aikakone", page_icon="🕰️", layout="wide")
wikipedia.set_lang("fi")

# --- Kuvat ---
# Tässä käytämme Wikimedia Commonsin julkisia kuvia. 
# Voit vaihtaa URL-osoitteet haluamiisi kuviin myöhemmin.
KUVA_KARTTA = "kuvax1.png"
KUVA_KIRKONKIRJA = "kuva2x.png"

def main():
    # --- Sivupalkki (Sidebar) ---
    with st.sidebar:
        st.image(KUVA_KIRKONKIRJA, caption="Tämän sivun tarjoaa SUKU -lehti")
        st.header("Tietoa")
        st.write("Tämä työkalu on tehty sukututkimuksen avuksi hahmottamaan historiallista kontekstia.")
        st.write("Lähde: Wikipedia")

    # --- Pääsisältö ---
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(KUVA_KARTTA, caption="1800-luvun tapahtumia Suomessa")

    with col2:
        st.title("🕰️ Sukututkijan Aikakone")
        st.markdown("**Syötä vuosiluku** (esim. 1868, 1918), niin näet mitä Suomessa ja maailmalla tapahtui.")

        # Hakukenttä
        vuosi = st.number_input("Valitse vuosi:", min_value=1000, max_value=2025, value=1900, step=1)
        hae_nappi = st.button("🔍 Hae tapahtumat")

    st.divider()

    if hae_nappi and vuosi:
        hae_tiedot(vuosi)

def hae_tiedot(vuosi):
    with st.spinner(f'Tutkitaan historiankirjoja vuodelta {vuosi}...'):
        try:
            sivu = wikipedia.page(str(vuosi))
            teksti = sivu.content
            
            # Jaetaan tulos kahteen sarakkeeseen
            c1, c2 = st.columns([1, 1])

            with c1:
                st.header(f"🇫🇮 Suomi ja maailma {vuosi}")
                st.success(sivu.summary)
                st.markdown(f"👉 **Lue lisää Wikipediasta:** [{sivu.url}]({sivu.url})")

            with c2:
                st.subheader("📜 Vuoden tapahtumat")
                
                # --- ÄLYKÄS LEIKKAUS ALKAA TÄSTÄ ---
                
                # 1. Etsitään mistä "Tapahtumia"-osio alkaa
                alku_indeksi = teksti.find("Tapahtumia")
                
                if alku_indeksi != -1:
                    # 2. Etsitään mihin se loppuu. Yleensä seuraava otsikko on "Syntyneitä".
                    # Jos "Syntyneitä" ei löydy, kokeillaan "Kuolleita".
                    loppu_indeksi = teksti.find("Syntyneitä", alku_indeksi)
                    
                    if loppu_indeksi == -1:
                        loppu_indeksi = teksti.find("Kuolleita", alku_indeksi)

                    # 3. Leikataan teksti talteen
                    if loppu_indeksi != -1:
                        # Otetaan kaikki tapahtumien ja syntyneiden välistä
                        ote = teksti[alku_indeksi:loppu_indeksi]
                    else:
                        # Jos loppukohtaa ei löydy, otetaan reilusti tekstiä (15 000 merkkiä)
                        # Tämä riittää varmasti loppuvuoteen asti.
                        ote = teksti[alku_indeksi : alku_indeksi + 15000]
                else:
                    # Jos koko "Tapahtumia" sanaa ei löydy, näytetään artikkelin alku
                    ote = teksti[:15000]

                # --- ÄLYKÄS LEIKKAUS PÄÄTTYY ---

                # Näytetään teksti vieritettävässä laatikossa
                st.text_area(
                    label="Tapahtumaluettelo:",
                    value=ote,
                    height=500,  # Kasvatettu hieman korkeutta
                    disabled=True
                )

        except wikipedia.exceptions.PageError:
            st.error(f"Vuodelta {vuosi} ei löytynyt suoraa artikkelia.")
        except Exception as e:
            st.error(f"Virhe haettaessa tietoja: {e}")

if __name__ == "__main__":

    main()




