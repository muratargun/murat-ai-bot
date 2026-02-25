import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Murat Argun AI", page_icon="💼", layout="centered")

# --- TEMA SAKLAMA ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

col1, col2 = st.columns([0.85, 0.15])
with col2:
    theme_choice = st.selectbox("Görünüm", ["Dark", "Light"], label_visibility="collapsed")
    st.session_state.theme = theme_choice

# --- RENK PALETLERİ VE BALON TASARIMLARI ---
if st.session_state.theme == "Dark":
    main_bg = "#0e1117"
    text_color = "#FFFFFF"
    user_bubble = "#262730"
    asst_bubble = "#1a1c23"
    border_color = "#333333"
    input_bg = "#1e1e24"
    select_bg = "#1e1e24"
    title_color = "#FFFFFF" # Dark modda başlık rengi
else:
    main_bg = "#F9FAFB"
    text_color = "#111827"
    user_bubble = "#E5E7EB"
    asst_bubble = "#FFFFFF"
    border_color = "#D1D5DB"
    input_bg = "#FFFFFF"
    select_bg = "#374151"
    title_color = "#111827" # Light modda başlık rengi

# --- CSS: YENİ BAŞLIK VE PROFESYONEL DOKUNUŞLAR ---
st.markdown(f"""
    <style>
    header, #MainMenu, footer {{visibility: hidden;}}

    /* Yeni Profesyonel Sol Üst Başlık */
    .new-pro-title {{
        position: fixed; /* Sayfada sabit durur, kaymaz */
        top: 20px;
        left: 25px;
        z-index: 999; /* Diğer öğelerin üstünde görünmesini sağlar */
    }}
    
    /* Başlığın içindeki "Murat Argun" kısmı (Koyu/Belirgin) */
    .title-name {{
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem; /* Mobilde daha küçük olacak */
        font-weight: 700;
        color: {title_color};
        margin: 0;
        letter-spacing: -0.02em;
    }}

    /* Başlığın içindeki "Dijital Asistan" kısmı (Hafif/Sade) */
    .title-role {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        color: {title_color};
        opacity: 0.7; /* Biraz daha soluk */
        margin: 0;
        margin-top: 2px;
    }}

    /* Mobil uyumluluk için medya sorgusu */
    @media (max-width: 600px) {{
        .new-pro-title {{
            top: 15px;
            left: 15px;
        }}
        .title-name {{
            font-size: 1rem; /* Mobilde daha küçük */
        }}
        .title-role {{
            font-size: 0.85rem; /* Mobilde daha küçük */
        }}
    }}

    div[data-baseweb="select"] > div {{
        background-color: {select_bg} !important;
        color: #FFFFFF !important; 
        border: none !important;
    }}
    li[role="option"] {{
        color: #FFFFFF !important;
    }}

    [data-testid="stChatMessageAvatarContainer"] {{
        display: none !important;
        width: 0 !important;
        margin: 0 !important;
    }}
    [data-testid="stChatMessage"] {{
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-bottom: 15px !important;
    }}

    .msg-user {{
        background-color: {user_bubble};
        color: {text_color};
        padding: 15px 20px;
        border-radius: 15px 15px 0px 15px;
        border: 1px solid {border_color};
        margin-left: auto;
        margin-right: 0;
        width: fit-content;
        max-width: 85%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    .msg-assistant {{
        background-color: {asst_bubble};
        color: {text_color};
        padding: 15px 20px;
        border-radius: 15px 15px 15px 0px;
        border: 1px solid {border_color};
        margin-left: 0;
        margin-right: auto;
        width: fit-content;
        max-width: 85%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    .msg-user p, .msg-assistant p {{
        margin-bottom: 0 !important;
    }}

    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {main_bg};
    }}
    [data-testid="stBottom"], [data-testid="stBottom"] > div {{
        background-color: {main_bg} !important;
    }}
    [data-testid="stChatInput"] {{
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    p, span, h1, textarea {{
        font-family: 'Inter', sans-serif !important;
        color: {text_color} !important;
        line-height: 1.6;
    }}

    /* Eski büyük başlığı gizle */
    .main-title {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MODEL KONFİGÜRASYONU ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except:
    st.error("API Anahtarı bulunamadı veya hatalı! Lütfen ayarlarınızı kontrol edin.")
    st.stop()
# --- SİSTEM TALİMATI (MURAT'I ANLATAN ASİSTAN) ---
PERSONAL_INFO = """
SEN KİMSİN?
Sen Murat Argun'un dijital asistanısın. Görevin, Murat'ı işe alım profesyonellerine tanıtmaktır.
Murat'ı tek boyutlu bir mühendis olarak değil; analitik zekasını sosyal becerileri, tasarım yeteneği ve stratejik bakış açısıyla birleştiren "çok yönlü" bir aday olarak konumlandırmalısın.

--- KATI KURALLAR & FORMAT ---
1. FORMAT: Asla HTML etiketi (blockquote, br, vb.) kullanma. Sadece düz metin.
2. PERSPEKTİF: Asla "ben" deme. Her zaman "Murat", "O" veya "Kendisi" de.
3. ÜSLUP: Profesyonel, saygılı ama samimi.

--- CEVAPLAMA STRATEJİLERİ ---

DURUM 1: GENEL TANIŞMA ("Murat kimdir?")
Şu kalıbı kullan: "Murat, ODTÜ'de 4. sınıf Endüstri Mühendisliği okuyor. Ankara'da yaşıyor. Eğitim hayatında WAT programı, projeler ve öğrenci topluluklarında aktif rol alarak kendini geliştirmiştir. Mühendislik formasyonunu; yaratıcı süreçler ve insan ilişkileriyle birleştirerek hem teknik hem de sosyal yönü güçlü bir profil çizer."

DURUM 2: DAVRANIŞSAL SORULAR (Liderlik, İnisiyatif, Zorluk) - *BURASI ÇOK ÖNEMLİ*
Bu sorularda şu 3 adımı izle:
1. ANA ÖRNEK: En güçlü örneği (Liderlik konusunda ODTÜ VT, zorluk konusunda WAT tecrübeleri, aldığı inisiyatifler ve yaptığı projeler konusunda BOSCH stajı ve ETİ Bitirme projelerinden bahset) özetle anlat.
2. YAN SİNYAL: "Bunun dışında diğer işlerinde de benzer sorumluluklar almıştır" diyerek diğer tecrübesine kısaca değin.
3. PAS ATMA (CALL TO ACTION): Detayları vermeden önce merak uyandır ve cevabı her zaman kendısıne ulaşarak deneyimlerini öğrenebilirsiniz de. "Bu süreçteki karar alma mekanizmasını ve hislerini, doğrudan kendisinden dinlemeniz, potansiyelini görmeniz açısından en doğrusu olacaktır" diyerek topu Murat'a at.

DURUM 3: KAPSAM DIŞI / KİŞİSEL SORULAR
Eğer soru Murat'ın profesyonel hayatı, projeleri veya eğitimiyle ilgili değilse (örneğin: en sevdiği yemek, tuttuğu takım vb.), doğrudan şu yanıtı ver:
"Bu asistan Murat'ın profesyonel portföyüne odaklandığı için sorduğunuz kişisel detaya dair bir bilgi sistemimde yer almıyor. Yine de kendisinin akademik başarıları, Bosch ve Eti projeleri veya pazarlama yetkinlikleri üzerine sorularınızı yanıtlamaktan memnuniyet duyarım. Murat'ın kariyer yolculuğuyla ilgili başka ne bilmek istersiniz?"

--- KATI KURALLAR ---
- Kişisel sorulara asla "Bilmiyorum" deyip bırakma; her zaman konuyu profesyonel bir alana (staj, ODTÜ, projeler) çekerek kapat.
- Cevaplar kısa ve öz olsun.
--- MURAT'IN BİLGİ BANKASI ---

1. ODTÜ VERİMLİLİK TOPLULUĞU (LİDERLİK & PAZARLAMA VURGUSU)
   * Dizayn Komitesi Koordinatörü olarak 20 kişilik ekibi yönetti.
   * Adobe Photoshop/Illustrator ile markanın görsel kimliğini ve dijital pazarlama stratejilerini oluşturdu.
   * WEQUAL projesinde sunuculuk yaparak kriz yönetimi ve topluluk önünde konuşma becerilerini sergiledi.

2. ETİ - BİTİRME PROJESİ (ANALİTİK & OPERASYONEL)
   * Konu: İç Lojistikte Araç ve Rota Planlamasının Otomasyonu.
   * Detay: Lojistik ağındaki rota verimliliğini maksimize eden algoritmalar geliştiriyor. 

3. BOSCH TÜRKİYE STAJI (ÜRETİM & PLANLAMA)
   * Büyük ölçekli üretim verilerini analiz edip tedarik zinciri süreçlerini iyileştiren bir algoritma tasarladı.
   * Zaman kısıtı altında bir projeyi tamamlamayı öğrendi.
   * İş akışı koordinasyonu konusunda kurumsal deneyim kazandı. Bunun yanında Excel ve Power Platforms uygulamalarını kullanmayı öğrendi.

4. WORK AND TRAVEL - ABD (SATIŞ & İLETİŞİM)
   * Hollywood Pictures bünyesinde fotoğrafçılık ve satış yaptı.
   * Kendi satış stratejilerini geliştirdi, farklı kültürdeki insanlara satış yaparak tecrübelendi.
   * Yüksek değerli satış süreçlerini yönetti, ikna kabiliyeti ve İngilizce pratiği kazandı.

5. EĞİTİM & TEKNİK
   * ODTÜ Endüstri Mühendisliği (2023-Güncel).
   * ODTÜ Makine Mühendisliği Geçmişi (2021-2023): Teknik ve analitik temel.
   * Güncel ortalaması: 2.66, Geçen dönem ortalaması: 3.50 ve yüksek onur öğrencisi (ortalama ve akademi sorulduğunda kesin olarak geçen dönem onur öğrencisi olduğu belirtilmeli)
   * Araçlar: Python, Microsoft Word, Microsoft Excel, MS Power Platforms, Adobe Creative Cloud, Google Ads, Siemens NX11.
   * Diller: İngilizce (İleri), Çince (Başlangıç).
   
6. İLETİŞİM BİLGİLERİ
   * Cep Telefonu: +90 546 243 53 72
   * Mail Adresi: muratt.argun@gmail.com
   * LinkedIn Profili: https://www.linkedin.com/in/murat-argun-667874269/
"""
# Görünmez piksel
EMPTY_AVATAR = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# --- YENİ SOL ÜST BAŞLIK ---
st.markdown(f"""
    <div class="new-pro-title">
        <h2 class="title-name">Murat Argun</h2>
        <p class="title-role">Dijital Asistan</p>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT MANTIĞI VE ARAYÜZ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben Murat Argun'un asistanıyım. Kariyeri veya projeleri hakkında ne bilmek istersiniz?"}]

# Geçmiş mesajları yeni balon yapısıyla ekrana basma
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=EMPTY_AVATAR):
        div_class = "msg-user" if message["role"] == "user" else "msg-assistant"
        st.markdown(f"<div class='{div_class}'>\n\n{message['content']}\n\n</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Murat hakkında bir soru sorun..."):
    # 1. Kullanıcı mesajını anında ekranda göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=EMPTY_AVATAR):
        st.markdown(f"<div class='msg-user'>\n\n{prompt}\n\n</div>", unsafe_allow_html=True)

    # 2. Bota hafıza ekleme (Geçmiş sohbetleri birleştir)
    chat_history = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        chat_history.append({"role": role, "parts": [msg["content"]]})

    # 3. Asistanın cevap verme süreci
    with st.chat_message("assistant", avatar=EMPTY_AVATAR):
        with st.spinner("Asistan yanıtlıyor..."):
            try:
                # 1.5 Flash modeli en kararlı ve hızlı sürümdür, donmaları engeller.
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PERSONAL_INFO)
                response = model.generate_content(chat_history)
                resp_text = response.text
            except Exception as e:
                try:
                    # Alternatif model
                    model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=PERSONAL_INFO)
                    response = model.generate_content(chat_history)
                    resp_text = response.text
                except Exception as e2:
                    # Artık donmak yerine sorunun ne olduğunu ekrana yazacak
                    resp_text = f"Sistemde geçici bir teknik sorun oluştu, lütfen sayfayı yenileyip tekrar deneyin. (Hata Kodu: {str(e2)})"
        
        # 4. Yükleme bitince asistan mesajını balon içinde göster ve kaydet
        st.markdown(f"<div class='msg-assistant'>\n\n{resp_text}\n\n</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": resp_text})
