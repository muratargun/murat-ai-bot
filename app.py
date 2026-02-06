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

    # --- AKILLI MODEL SEÇİCİ (SELF-HEALING) ---
    try:
        # 1. Hesabının görebildiği TÜM modelleri çek
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        target_model = None
        
        # 2. Modelleri filtrele: "2.0" olanlar paralı/kotalı olabilir, onlardan kaç. "1.5" ve "flash" olanı bul.
        # Öncelik sırası: 1.5-flash -> 1.5-pro -> flash-latest -> herhangi bir model
        for m in available_models:
            if "1.5" in m and "flash" in m and "002" not in m: # 002 bazen deneysel oluyor
                target_model = m
                break
        
        # Eğer 1.5-flash bulamazsa 1.5-pro dene
        if not target_model:
            for m in available_models:
                if "1.5" in m and "pro" in m:
                    target_model = m
                    break
        
        # Hala bulamadıysa gemini-pro (eski güvenilir) kullan
        if not target_model:
            target_model = "models/gemini-pro"

        # 3. Seçilen modeli kullan
        # st.caption(f"🔧 Kullanılan Model: {target_model}") # Debug için (istersen açabilirsin)
        
        model = genai.GenerativeModel(target_model, system_instruction=PERSONAL_INFO)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error("Bağlantı kurulamadı.")
        st.info("Lütfen Streamlit panelinden 'Reboot App' yapın.")
        # Hata detayını sadece sen gör diye expander içine koydum
        with st.expander("Teknik Hata Detayı"):
            st.write(e)
            st.write("Erişilebilen Modeller Listesi:")
            try:
                st.write([m.name for m in genai.list_models()])
            except:
                st.write("Liste alınamadı.")
