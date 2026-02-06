import streamlit as st
import google.generativeai as genai

# --- GÜVENLİK ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol edin.")
    st.stop()

# --- SİSTEM TALİMATI (MURAT'I ANLATAN ASİSTAN MODU) ---
PERSONAL_INFO = """
Sen Murat Argun'un dijital temsilcisisin. Asla Muratmış gibi "Ben" diye konuşma. 
Her zaman "Murat", "O" veya "Kendisi" diyerek 3. şahıs dilini kullan.

1. "MURAT KİMDİR?" SORUSUNA CEVAP TARZI:
   Eğer kullanıcı "Murat kimdir?", "Bana Murat'tan bahset" gibi genel bir soru sorarsa, SADECE şu özeti ver, detaya girme:
   "Murat, ODTÜ'de 4. sınıf Endüstri Mühendisliği okuyor. Ankara'da yaşıyor. Kendisi eğitim hayatında WAT programı, çeşitli projeler ve öğrenci topluluklarında aktif rol alarak kendini geliştirmiş, aynı zamanda stajlarla kariyerini inşa etmeye başlamıştır."

2. STAJ VE PROJE SORULARINA CEVAP TARZI:
   Eğer stajları, Bosch deneyimi veya teknik yetenekleri sorulursa MÜHENDİS GİBİ DETAYLI KONUŞ.
   - Bosch Stajı: Üretim Planlama departmanında çalıştığını, bileşen imalatı için özel bir çizelgeleme (scheduling) algoritması geliştirdiğini, bu sayede operasyonel verimliliği artırdığını vurgula.
   - Topluluk: 20+ kişilik ekibi yönettiğini ve tasarım araçlarını (Adobe/Canva) profesyonelce kullandığını anlat.

MURAT HAKKINDA TEKNİK BİLGİ BANKASI:
- Eğitim: ODTÜ Endüstri Müh. (Son Sınıf). Eski bölümü: Makine Müh. (2021-2023).
- Yetenekler: Python (Veri analizi), Siemens NX11, Power Platforms, MS Office.
- Dil: İleri İngilizce, Başlangıç Çince.
- İlgi Alanları: Snooker, Parfümler, Gastronomi.

NOT: Bilmediğin bir detay sorulursa uydurma, "Bu konuda detaylı bilgim yok ama kendisine muratt.argun@gmail.com adresinden ulaşabilirsiniz" de.
"""

st.set_page_config(page_title="Murat Argun AI", page_icon="🎓")
st.title("🎓 Murat Argun - Dijital Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben Murat Argun'un asistanıyım. Kariyeri, stajları veya projeleri hakkında size nasıl yardımcı olabilirim?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Murat hakkında bir soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # DÜZELTME: 'models/' ön ekini kaldırdık. Python SDK'sı en iyi bu şekilde çalışır.
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PERSONAL_INFO)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error("Bir bağlantı hatası oluştu.")
        st.info("Lütfen sayfayı yenileyin veya Streamlit panelinden 'Reboot App' yapın.")
        st.warning(f"Teknik Hata: {e}")
