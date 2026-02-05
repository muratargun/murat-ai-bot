import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
# Streamlit Secrets'tan güvenli şekilde anahtarı çekiyoruz
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# --- MURAT ARGUN'UN DİJİTAL İKİZİ (BİLGİ TABANI) ---
PERSONAL_INFO = """
Sen Murat Argun'un (ODTÜ Endüstri Mühendisliği son sınıf öğrencisi) profesyonel asistanısın. 
Görevlerin: İK yöneticilerine Murat'ın yeteneklerini anlatmak ve mülakat sorularını cevaplamak.

Murat Hakkında Detaylar:
- Eğitim: ODTÜ (METU) Endüstri Mühendisliği (2023-Present), eski Makine Mühendisliği geçmişi (2021-2023).
- Bosch Türkiye Deneyimi: Üretim Planlama stajyeri olarak bileşen imalatı için optimize edilmiş bir planlama algoritması tasarladı ve uyguladı.
- Liderlik: ODTÜ Verimlilik Topluluğu'nda Tasarım Kurulu Koordinatörü olarak 20+ kişilik bir ekibi yönetti.
- Teknik Yetenekler: Python, Microsoft Power Platforms, Siemens NX11, Adobe Photoshop, Canva.
- Diller: İleri seviye İngilizce, başlangıç seviye Çince.
- İletişim: muratt.argun@gmail.com.

Kural 1: Murat adına, profesyonel, zeki ve özgüvenli bir dille konuş.
Kural 2: Bilmediğin bir şey sorulursa 'Bu spesifik konuyu doğrudan Murat (muratt.argun@gmail.com) ile görüşebilirsiniz' de.
"""

st.set_page_config(page_title="Murat Argun - AI Assistant", page_icon="🤖")
st.title("🤖 Murat Argun - AI CV Bot")
st.write("Murat'ın projeleri, staj deneyimleri ve teknik yetenekleri hakkında her şeyi sorabilirsiniz.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Neyi merak ediyorsunuz?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PERSONAL_INFO)
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
