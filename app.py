import streamlit as st
import wikipedia

# Asetukset
st.set_page_config(page_title="Sukututkijan Aikakone", page_icon="🕰️", layout="wide")
wikipedia.set_lang("fi")

# Kuvat (käytetään varmoja linkkejä tai paikallisia tiedostoja)
# Jos kuvat eivät näy, voit kommentoida nämä rivit pois (laita # eteen)
KUVA_KARTTA = "kuvax1.png"
KUVA_KIRKONKIRJA = "kuva2x.png" 

def main():
    # --- Sivupalkki ---
    with st.sidebar:
        # Näytetään kuva vain jos linkki toimii, muuten ohitetaan virhe
        try:
            st.image(KUVA_KIRKONKIRJA, caption="Sivun tarjoaa SUKU -lehti")
        except:
            st.write("Kuvaa ei voitu ladata.")
            
        st.header("Tietoa")
        st.write("Tämä työkalu hakee tiedot Wikipediasta ja auttaa sijoittamaan esivanhemmat aikaansa.")

    # --- Pääsisältö ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(KUVA_KARTTA, caption="SUKU - lehti sukututkijoille")
        except:
            st.write("Karttakuvaa ei voitu ladata.")

    with col2:
        st.title("🕰️ Sukututkijan Aikakone")
        st.markdown("**Syötä vuosiluku**, niin näet vuoden tapahtumat.")

        vuosi = st.number_input("Valitse vuosi:", min_value=1000, max_value=2025, value=1900, step=1)
        hae_nappi = st.button("🔍 Hae tapahtumat")

    st.divider()

    if hae_nappi and vuosi:
        hae_tiedot(vuosi)

def hae_tiedot(vuosi):
    with st.spinner(f'Tutkitaan historiankirjoja vuodelta {vuosi}...'):
        try:
            # Haetaan sivu
            sivu = wikipedia.page(str(vuosi))
            teksti = sivu.content # Haetaan koko sivun raakateksti
            
            # 1. Yhteenveto vasemmalle
            c1, c2 = st.columns([1, 1])

            with c1:
                st.header(f"🇫🇮 Yhteenveto {vuosi}")
                st.success(sivu.summary)
                st.markdown(f"👉 **Lue koko artikkeli Wikipediasta:** [{sivu.url}]({sivu.url})")

            # 2. Pitkä sisältö oikealle
            with c2:
                st.subheader("📜 Tapahtumaluettelo")
                
                # --- UUSI LOGIIKKA: NÄYTETÄÄN KAIKKI ---
                # Yritetään löytää kohta missä varsinaiset tapahtumat alkavat,
                # jotta emme toista yhteenvetoa.
                
                aloitus_kohdat = ["== Tapahtumia ==", "Tapahtumia", "== Tapahtumat =="]
                aloitus_indeksi = 0
                
                for hakusana in aloitus_kohdat:
                    kohta = teksti.find(hakusana)
                    if kohta != -1:
                        aloitus_indeksi = kohta
                        break
                
                # Otetaan teksti aloituskohdasta ihan loppuun asti.
                # Ei yritetä leikata loppua pois, jotta mitään ei varmasti katoa.
                lopullinen_teksti = teksti[aloitus_indeksi:]
                
                # Jos teksti on valtava, rajoitetaan se 30 000 merkkiin (riittää varmasti)
                if len(lopullinen_teksti) > 30000:
                    lopullinen_teksti = lopullinen_teksti[:30000] + "\n... (teksti jatkuu Wikipediassa)"

                st.text_area(
                    label="Selaa vuoden tapahtumia:",
                    value=lopullinen_teksti,
                    height=600,  # Iso ikkuna
                    disabled=False
                )

        except wikipedia.exceptions.PageError:
            st.error(f"Vuodelta {vuosi} ei löytynyt suoraa artikkelia.")
        except Exception as e:
            st.error(f"Tapahtui virhe: {e}")

if __name__ == "__main__":
    main()




