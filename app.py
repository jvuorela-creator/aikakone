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
            
            # Jaetaan tulos kahteen sarakkeeseen
            c1, c2 = st.columns([1, 1])

            with c1:
                st.header(f"🇫🇮 Suomi ja maailma {vuosi}")
                st.success(sivu.summary)
                st.markdown(f"👉 **Lue lisää Wikipediasta:** [{sivu.url}]({sivu.url})")

            with c2:
                teksti = sivu.content
                st.subheader("📜 Poimintoja arkistoista")
                
                # Etsitään "Tapahtumia"-kohta
                if "Tapahtumia" in teksti:
                    alku = teksti.find("Tapahtumia")
                    # Otetaan reilusti tekstiä (1500 merkkiä), jotta luettavaa riittää
                    ote = teksti[alku:alku+1500] 
                else:
                    ote = teksti[:1000]

                # TÄMÄ ON MUUTETTU KOHTA:
                # Käytetään text_area-komentoa ja height-asetusta.
                # height=400 määrää laatikon korkeuden pikseleinä.
                st.text_area(
                    label="Tapahtumaluettelo:",
                    value=ote,
                    height=400,  # Tässä määritellään vierityskehyksen korkeus
                    disabled=True # Estää tekstin muokkaamisen (tekee siitä "lukutilan")
                )

        except wikipedia.exceptions.PageError:
            st.error(f"Vuodelta {vuosi} ei löytynyt suoraa artikkelia.")
        except Exception as e:
            st.error(f"Virhe haettaessa tietoja: {e}")

if __name__ == "__main__":

    main()

