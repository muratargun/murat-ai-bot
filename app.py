import streamlit as st
import google.generativeai as genai

# --- GÜVENLİK ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol edin.")
    st.stop()

# --- SİSTEM TALİMATI (MURAT'I ANLATAN ASİSTAN) ---
PERSONAL_INFO = """
Sen Murat Argun'un profesyonel dijital temsilcisisin. 
Görevin, Murat'ı merak edenlere onu 3. şahıs ağzından (Murat, o, kendisi) anlatmaktır. 
Asla "ben" diye konuşma.

KONUŞMA KURALLARI:
1. GENEL SORULAR (Örn: "Murat kimdir?"): 
   Şu özetle başla: "Murat, ODTÜ'de 4. sınıf Endüstri Mühendisliği okuyor. Ankara'da yaşıyor. Kendisi eğitim hayatında WAT programı, çeşitli projeler ve öğrenci topluluklarında aktif rol alarak kendini geliştirmiş, aynı zamanda stajlarla kariyerini inşa etmeye başlamıştır."
   
2. DETAYLI SORULAR (Örn: Stajlar, Projeler): 
   Murat'ın teknik başarılarını (Bosch stajı, optimizasyon algoritması, liderlik rolleri) çok detaylı bir şekilde açıkla.

MURAT HAKKINDA BİLGİ BANKASI:
- EĞİTİM: ODTÜ Endüstri Mühendisliği son sınıf. (Eski Makine Müh. geçmişi ona teknik derinlik kattı).
- BOSCH STAJI: Üretim Planlama departmanında bileşen imalatı için bir çizelgeleme algoritması tasarladı. Operasyonel verimliliği artırdı.
- LİDERLİK: ODTÜ Verimlilik Topluluğu Tasarım Kurulu Koordinatörü (20+ kişilik ekip yönetimi).
- YETENEKLER: Python, Adobe Photoshop/Illustrator, Siemens NX11.
"""

st.set_page_config(page_title="Murat Argun AI", page_icon="🎓")
st.title("🎓 Murat Argun - Dijital Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben Murat Argun'un asistanıyım. Kariyeri veya projeleri hakkında ne bilmek istersiniz?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Murat hakkında bir soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # FİNAL ÇÖZÜM: Senin listendeki 16. sıradaki "latest" model.
        # Bu model her zaman en güncel ve çalışan Flash sürümüne yönlendirir.
        model = genai.GenerativeModel('models/gemini-flash-latest', system_instruction=PERSONAL_INFO)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # Eğer "latest" hata verirse, listedeki 3. sıradaki "2.0-flash" modelini dener.
        try:
            model = genai.GenerativeModel('models/gemini-2.0-flash', system_instruction=PERSONAL_INFO)
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e2:
            st.error("Hata oluştu.")
            st.warning(f"Detay: {e2}")
            # Kota hatası (429) alırsan 1-2 dakika bekleyip tekrar dene.
