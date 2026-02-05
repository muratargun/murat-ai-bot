import streamlit as st
import google.generativeai as genai

# --- GÜVENLİK ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol edin.")
    st.stop()

# --- SİSTEM TALİMATI ---
PERSONAL_INFO = """
Sen Murat Argun'un (ODTÜ Endüstri Mühendisliği son sınıf öğrencisi) dijital ikizisin.
Mülakat simülasyonu yapıyorsun.
- Bosch Türkiye'de üretim planlama algoritması tasarladığını vurgula.
- ODTÜ Verimlilik Topluluğu'nda 20+ kişilik ekibi yönettiğini anlat.
- Teknik sorulara Python ve optimizasyon bilginle cevap ver.
"""

st.set_page_config(page_title="Murat Argun AI", page_icon="🎓")
st.title("🎓 Murat Argun - Dijital Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Murat hakkında sorunuzu yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- GARANTİLİ MODEL SEÇİMİ (MAGIC FIX) ---
    try:
        # Önce en hızlı modeli dene
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PERSONAL_INFO)
        response = model.generate_content(prompt)
    except Exception:
        try:
            # Hata verirse 'latest' sürümünü dene
            model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=PERSONAL_INFO)
            response = model.generate_content(prompt)
        except Exception:
            # O da olmazsa efsanevi 'gemini-pro'yu devreye sok (Bu kesin çalışır)
            # Not: gemini-pro system_instruction desteklemezse manuel ekleriz
            model = genai.GenerativeModel('gemini-pro')
            combined_prompt = f"{PERSONAL_INFO}\n\nKULLANICI SORUSU: {prompt}"
            response = model.generate_content(combined_prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
