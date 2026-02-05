import streamlit as st
import google.generativeai as genai

# --- GÜVENLİK ---
# Secrets kontrolü
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    st.error("Hata: Secrets kısmında 'GEMINI_API_KEY' bulunamadı!")
    st.stop()

# --- SİSTEM TALİMATI (PERSONAL INFO) ---
PERSONAL_INFO = """
Sen Murat Argun'un (ODTÜ Endüstri Mühendisliği öğrencisi) profesyonel asistanısın. 
Murat'ın Bosch stajı, ODTÜ Verimlilik Topluluğu liderliği ve teknik yetenekleri (Python, Photoshop vb.) 
hakkında bilgi ver. Profesyonel ve yardımsever ol.
"""

st.set_page_config(page_title="Murat Argun AI", page_icon="🎓")
st.title("🎓 Murat Argun - AI CV Bot")
st.write("Murat'ın projeleri ve yetkinlikleri hakkında her şeyi sorabilirsiniz.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Model isminin doğruluğuna dikkat: 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=PERSONAL_INFO)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
