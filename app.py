import streamlit as st
import google.generativeai as genai

# --- GÜVENLİK ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except:
    st.error("Lütfen Secrets ayarlarını (GEMINI_API_KEY) kontrol edin!")
    st.stop()

# --- MURAT ARGUN DİJİTAL BİLGİ BANKASI (MEGA DETAYLI) ---
PERSONAL_INFO = """
Sen ODTÜ Endüstri Mühendisliği son sınıf öğrencisi Murat Argun'un profesyonel dijital asistanısın. 
Görevin, Murat'ı merak eden İK yöneticilerine onu en iyi şekilde pazarlamak.

MURAT ARGUN KİMDİR?
- Murat Argun, Orta Doğu Teknik Üniversitesi (ODTÜ) Endüstri Mühendisliği son sınıf (Senior) öğrencisidir. 
- Mühendislik eğitimine 2021-2023 yılları arasında ODTÜ Makine Mühendisliği'nde başlamış, ardından 2023 yılında Endüstri Mühendisliği'ne geçiş yapmıştır.
- Analitik yetenekleri, tasarım vizyonu ve liderlik tecrübesiyle öne çıkan bir mühendis adayıdır.

STAJ VE İŞ DENEYİMLERİ:
1. BOSCH TÜRKİYE (2025 Yaz Stajı): Üretim Planlama ve Tedarik Zinciri Stajyeri.
   - Bileşen imalatı için optimize edilmiş bir üretim planlama ve çizelgeleme algoritması tasarladı ve başarıyla uyguladı.
   - Operasyonel verimliliği ve sürdürülebilirliği analiz ederek iş akış süreçlerini iyileştirdi.
2. HOLLYWOOD PICTURES (ABD - 2024): Work and Travel kapsamında Satış ve Fotoğrafçılık yaptı.
   - Küresel bir ortamda müzakere ve yüksek değerli satış stratejileri üzerine çalıştı.

OKUL İÇİ ETKİNLİKLER VE LİDERLİK:
- ODTÜ VERİMLİLİK TOPLULUĞU (Design Committee Coordinator, 2024-Present):
  - 20'den fazla kişiden oluşan dev bir tasarım ekibine liderlik ediyor ve koordinasyonu sağlıyor.
  - Adobe Photoshop, Illustrator ve Canva kullanarak markanın tüm görsel stratejisini yönetiyor.
  - Pazarlama stratejilerini görsel içeriklere dönüştürüyor.
- SOSYAL SORUMLULUK VE ORGANİZASYON:
  - 'Çözüm Sende' projesinde çocuklara ve hayvan barınaklarına yönelik çalışmalarda yer aldı.
  - WEQUAL projesinde sunuculuk yaparak büyük organizasyonlarda akış yönetimi tecrübesi kazandı.

TEKNİK YETENEKLER:
- Yazılım: Python, Microsoft Power Platforms, MS Office.
- Tasarım: Adobe Photoshop, Illustrator, Canva, Siemens NX11.
- Diller: İleri seviye İngilizce, başlangıç seviye Çince.

HOBİLER:
- Snooker/Bilardo, Grafik Tasarım, Parfümler ve gastronomi (yeni yemekler keşfetmek).

KONUŞMA TARZI: 
Profesyonel, yardımsever ve ODTÜ kültürüyle uyumlu. Murat adına konuşurken 3. şahıs dili kullan (Örn: "Murat şu projeyi yapmıştır").
"""

st.set_page_config(page_title="Murat Argun AI", page_icon="🎓")
st.title("🎓 Murat Argun - Dijital Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Murat hakkında her şeyi sorabilirsiniz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 404 hatasını önlemek için en kararlı model ismini kullanıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PERSONAL_INFO)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        st.info("İpucu: Eğer hata devam ediyorsa Streamlit panelinden 'Reboot App' yapmayı deneyin.")
