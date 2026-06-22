import streamlit as st
from google import genai
from PIL import Image
import io

# Konfiguracja PWA i wyglądu
st.set_page_config(page_title="A co to?", page_icon="👁️‍🗨️", layout="centered")

st.title("👁️‍🗨️ A co to?")
st.write("Zrób zdjęcie robaka, kamienia, budynku lub czegokolwiek, co Cię zaciekawiło, a AI odpowie na Twoje pytanie!")

# Klucz API w sidebarze
with st.sidebar:
    st.header("⚙️ Ustawienia")
    api_key = st.text_input("Wprowadź Google Gemini API Key:", type="password")
    st.markdown("[Pobierz darmowy klucz stąd](https://aistudio.google.com/)")

# Wybór trybu
mode = st.radio(
    "Kto pyta?",
    ["👶 Tryb Młodego Odkrywcy (Dla dzieci)", "🧐 Tryb Naukowy (Dla rodziców)"]
)

# Aparat i lokalizacja
img_file = st.camera_input("📸 Skieruj oko lupy na obiekt")
if not img_file:
    img_file = st.file_uploader("Lub wybierz zdjęcie z galerii telefonu", type=["jpg", "jpeg", "png"])

location = st.text_input("📍 Gdzie to znalazłeś/aś? (np. Las, park, plaża, miasto)")

if st.button("Zbadaj znalezisko! 🚀", type="primary"):
    if not api_key:
        st.error("Wpisz swój klucz API w panelu bocznym!")
    elif not img_file:
        st.error("Najpierw musisz zrobić lub dodać zdjęcie!")
    else:
        with st.spinner("Oko lupy analizuje Twój skarb..."):
            try:
                # Inicjalizacja klienta
                client = genai.Client(api_key=api_key)
                image_data = img_file.read()
                image = Image.open(io.BytesIO(image_data))
                
                if "Młodego Odkrywcy" in mode:
                    prompt = f"""
                    Jesteś zabawnym, pełnym energii Profesorem Przygoda. Rozmawiasz z dociekliwym dzieckiem, które pyta "A co to?".
                    Zidentyfikuj obiekt na zdjęciu (lokalizacja: {location}).
                    Napisz odpowiedź w prosty, fascynujący sposób. Używaj emotikonów.
                    Podziel odpowiedź na sekcje:
                    - 🌟 CO TO ZA SKARB? (Prosta, ciekawa nazwa)
                    - 🤫 SUPERMOC / SEKRET (Coś niesamowitego o tym obiekcie)
                    - 🎮 ZADANIE DLA CIEBIE (Prosta misja terenowa dla dziecka)
                    """
                else:
                    prompt = f"""
                    Działasz jako poważny przewodnik, biolog i ekspert. Rozmawiasz z rodzicem, który chce zaimponować dziecku wiedzą.
                    Zidentyfikuj obiekt na zdjęciu (lokalizacja: {location}).
                    Podziel odpowiedź na sekcje:
                    - 📌 Oficjalna nazwa (polska i łacińska)
                    - 🔍 Konkretne fakty i cechy
                    - 🗺️ Czy to pasuje do lokalizacji: {location}?
                    - 💡 Warto wiedzieć (Gotowa ciekawostka do opowiedzenia dziecku)
                    """

                # ZMIANA NA MODEL PRO DLA WYŻSZEJ STABILNOŚCI
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                
                st.success("Analiza zakończona!")
                st.markdown(response.text)
                
            except Exception as e:
                # Wyświetlamy pełny, czysty błąd użytkownikowi
                st.error("Wystąpił problem z analizą:")
                st.code(str(e))
