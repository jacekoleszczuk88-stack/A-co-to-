import streamlit as st
from google import genai
from PIL import Image
import io

# Konfiguracja PWA i wyglądu
st.set_page_config(page_title="Wakacyjny Odkrywca", page_icon="🤠", layout="centered")

st.title("🤠 Wakacyjny Odkrywca AI")
st.write("Zrób zdjęcie czegokolwiek (robaka, skały, budynku), a AI zdradzi Ci jego tajemnice!")

# Klucz API w sidebarze (dla bezpieczeństwa)
with st.sidebar:
    st.header("⚙️ Ustawienia")
    api_key = st.text_input("Wprowadź Google Gemini API Key:", type="password")
    st.markdown("[Pobierz darmowy klucz stąd](https://aistudio.google.com/)")

# Wybór trybu - to nas wyróżnia!
mode = st.radio(
    "Kto pyta?",
    ["👶 Tryb Młodego Odkrywcy (Prosty język, ciekawostki)", "🧐 Tryb Naukowy dla Rodziców (Konkrety, fakty)"]
)

# Aparat / Galeria
img_file = st.camera_input("📸 Zrób zdjęcie znaleziska")
if not img_file:
    img_file = st.file_uploader("Lub wybierz z galerii", type=["jpg", "jpeg", "png"])

location = st.text_input("📍 Gdzie to znalazłeś? (np. Plaża w Rowach, las, stare miasto)")

if st.button("Uruchom Skaner AI 🚀", type="primary"):
    if not api_key:
        st.error("Wpisz swój klucz API w panelu bocznym!")
    elif not img_file:
        st.error("Zrób lub dodaj zdjęcie!")
    else:
        with st.spinner("Skanowanie w toku..."):
            try:
                client = genai.Client(api_key=api_key)
                image_data = img_file.read()
                image = Image.open(io.BytesIO(image_data))
                
                # Dynamiczny prompt w zależności od wybranego trybu
                if "Młodego Odkrywcy" in mode:
                    prompt = f"""
                    Jesteś zabawnym, pełnym energii Profesorem Przygoda. Rozmawiasz z dzieckiem.
                    Zidentyfikuj obiekt na zdjęciu (lokalizacja: {location}).
                    Napisz odpowiedź w prosty, fascynujący sposób. Używaj emotikonów.
                    Podziel odpowiedź na sekcje:
                    - 🌟 CO TO ZA SKARB? (Prosta nazwa i opis)
                    - 🤫 SUPERMOC / CIEKAWOSTKA (Coś, co zszokuje dziecko)
                    - 🎮 ZADANIE DLA CIEBIE (Wymyśl prostą zabawę związaną z tym obiektem, np. 'Znajdź jeszcze 3 okrągłe kamienie')
                    """
                else:
                    prompt = f"""
                    Działasz jako poważny przewodnik, biolog i architekt. Rozmawiasz z rodzicem.
                    Zidentyfikuj obiekt na zdjęciu (lokalizacja: {location}).
                    Podziel odpowiedź na sekcje:
                    - 📌 Nazwa polska i łacińska / architektoniczna
                    - 🔍 Szczegóły techniczne / biologiczne
                    - 🗺️ Kontekst lokalny (Czy to typowe dla miejsca: {location})
                    - 💡 Warto wiedzieć (Fakty, którymi rodzic może zaimponować dziecku)
                    """

                response = client.models.generate_content(
                   model='gemini-1.5-flash',
                    contents=[image, prompt]
                )
                
                st.success("Skanowanie zakończone!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Błąd: {e}")
