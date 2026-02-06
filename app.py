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

    # --- ÇİLİNGİR MODU: HER KAPIYI DENEYEN KOD ---
    response = None
    error_log = []
    
    # Denenecek model isimleri sırasıyla:
    candidate_models = [
        'gemini-1.5-flash',          # En standart isim
        'models/gemini-1.5-flash',   # Bazı versiyonların istediği isim
        'gemini-1.5-flash-latest',   # Alternatif isim
        'gemini-1.5-flash-001'       # Versiyon numaralı isim
    ]

    with st.chat_message("assistant"):
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name, system_instruction=PERSONAL_INFO)
                response = model.generate_content(prompt)
                # Eğer buraya geldiyse hata yok demektir, döngüyü kır.
                break 
            except Exception as e:
                # Hata aldıysa bir sonraki isme geç
                error_log.append(str(e))
                continue
        
        if response:
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            # Tüm denemeler başarısız olursa
            st.error("Üzgünüm, şu an bağlantı kurulamadı.")
            st.code("\n".join(error_log)) # Teknik hata detayını göster
