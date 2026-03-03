import streamlit as st
import google.generativeai as genai
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Murat Argun AI", page_icon="💼", layout="centered")

# --- TEMA VE HIZLI SORU (STATE) SAKLAMA ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# --- RENK PALETLERİ VE BALON TASARIMLARI ---
# (Renkler arayüz kodundan önce tanımlanmalı ki üst barda kullanılabilsin)
if st.session_state.theme == "Dark":
    main_bg = "#0e1117"
    text_color = "#FFFFFF"
    user_bubble = "#262730"
    asst_bubble = "#1a1c23"
    border_color = "#333333"
    input_bg = "#1e1e24"
    select_bg = "#1e1e24"
    select_list_bg = "#1e1e24"
    title_color = "#FFFFFF"
    btn_bg = "#1e1e24"
    btn_text = "#FFFFFF"
else:
    main_bg = "#F9FAFB"
    text_color = "#111827"
    user_bubble = "#E5E7EB"
    asst_bubble = "#FFFFFF"
    border_color = "#D1D5DB"
    input_bg = "#FFFFFF"
    select_bg = "#FFFFFF"
    select_list_bg = "#FFFFFF"
    title_color = "#111827"
    btn_bg = "#FFFFFF"
    btn_text = "#111827"

# --- ÜST BAR (BAŞLIK, CV İNDİRME VE TEMA SEÇİMİ) ---
# Sütun oranlarını masaüstü için optimize ettik. Mobilde otomatik alt alta dizilecekler.
col1, col2, col3 = st.columns([0.55, 0.25, 0.20])

with col1:
    st.markdown(f"""
        <div class="new-pro-title">
            <h2 class="title-name">Murat Argun</h2>
            <p class="title-role">Dijital Asistan</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    try:
        with open("Murat Argun Resume.pdf", "rb") as pdf_file:
            cv_byte = pdf_file.read()
        st.download_button(
            label="📄 CV'mi İndir",
            data=cv_byte,
            file_name="Murat Argun Resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except FileNotFoundError:
        st.download_button(
            label="📄 CV'mi İndir",
            data=b"CV dosyasi bulunamadi.",
            file_name="hata_raporu.txt",
            use_container_width=True
        )

with col3:
    theme_choice = st.selectbox("Görünüm", ["Dark", "Light"], label_visibility="collapsed")
    st.session_state.theme = theme_choice

# --- CSS: TASARIM, BAŞLIK VE BUTONLAR ---
st.markdown(f"""
    <style>
    header, #MainMenu, footer {{visibility: hidden;}}

    /* BAŞLIK DÜZENLEMESİ (Fixed kaldırıldı, grid'e uyumlu hale getirildi) */
    .new-pro-title {{
        margin-top: 5px;
    }}
    .title-name {{
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem; 
        font-weight: 700;
        color: {title_color};
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .title-role {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        color: {title_color};
        opacity: 0.7; 
        margin: 0;
        margin-top: 2px;
    }}

    /* MOBİL GÖRÜNÜM AYARLARI */
    @media (max-width: 600px) {{
        .new-pro-title {{
            text-align: center;
            margin-bottom: 15px;
            margin-top: 0px;
        }}
        .title-name {{font-size: 1.6rem;}}
        .title-role {{font-size: 1.1rem;}}
    }}

    /* SELECTBOX KUTUSU VE AÇILIR MENÜ STİLLERİ */
    div[data-baseweb="select"] > div {{
        background-color: {select_bg} !important;
        color: {text_color} !important; 
        border: 1px solid {border_color} !important;
    }}
    div[role="listbox"], 
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"] {{
        background-color: {select_list_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    li[role="option"] {{ 
        color: {text_color} !important;
        background-color: {select_list_bg} !important;
    }}
    li[role="option"]:hover {{ 
        background-color: {user_bubble} !important; 
    }}

    /* BUTON VE CV İNDİRME BÖLÜMÜ STİLLERİ */
    div.stButton > button, div.stDownloadButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {border_color} !important;
    }}
    div.stButton > button p, div.stDownloadButton > button p {{
        color: {btn_text} !important;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        border-color: {text_color} !important;
        opacity: 0.8;
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
    .msg-user p, .msg-assistant p {{ margin-bottom: 0 !important; }}

    .stApp, [data-testid="stAppViewContainer"] {{ background-color: {main_bg}; }}
    [data-testid="stBottom"], [data-testid="stBottom"] > div {{ background-color: {main_bg} !important; }}
    
    /* CHAT INPUT İÇİ STİLLERİ */
    [data-testid="stChatInput"] {{
        background-color: {main_bg} !important;
    }}
    [data-testid="stChatInput"] > div {{
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    [data-testid="stChatInput"] div[data-baseweb="textarea"],
    [data-testid="stChatInput"] div[data-baseweb="base-input"],
    [data-testid="stChatInput"] div[data-baseweb="input"] {{
        background-color: {input_bg} !important;
    }}
    [data-testid="stChatInput"] textarea {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
        -webkit-text-fill-color: {text_color} !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {text_color} !important;
        opacity: 0.6 !important;
    }}
    [data-testid="stChatInput"] button {{
        background-color: transparent !important;
    }}
    [data-testid="stChatInput"] svg {{
        fill: {text_color} !important;
        color: {text_color} !important;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    p, span, h1, textarea {{
        font-family: 'Inter', sans-serif !important;
        color: {text_color} !important;
        line-height: 1.6;
    }}
    .main-title {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- MODEL KONFİGÜRASYONU ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except:
    st.error("API Anahtarı bulunamadı veya hatalı! Lütfen ayarlarınızı kontrol edin.")
    st.stop()

# --- SİSTEM TALİMATI ---
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

EMPTY_AVATAR = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# --- CHAT MANTIĞI VE ARAYÜZ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben Murat Argun'un asistanıyım. Kariyer, staj deneyimleri veya teknik yetkinlikler hakkında ne bilmek istersiniz?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=EMPTY_AVATAR):
        div_class = "msg-user" if message["role"] == "user" else "msg-assistant"
        st.markdown(f"<div class='{div_class}'>\n\n{message['content']}\n\n</div>", unsafe_allow_html=True)

# --- HIZLI SORU BUTONLARI ---
if len(st.session_state.messages) == 1:
    st.markdown(f"<div style='margin-bottom: 10px; color: {text_color}; opacity: 0.8; font-size: 0.9rem;'>💡 <b>Hızlı Sorular:</b> Aşağıdaki konuları seçerek sohbete başlayabilirsiniz:</div>", unsafe_allow_html=True)
    
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        if st.button("Murat Argun Kimdir?", use_container_width=True):
            st.session_state.quick_prompt = "Murat Argun kimdir? Kısaca vizyonundan ve yetkinliklerinden bahseder misin?"
            st.rerun()
    with q_col2:
        if st.button("Projeler ve Stajlar", use_container_width=True):
            st.session_state.quick_prompt = "Murat'ın yaptığı projeler ve staj deneyimleri (Bosch, Eti vb.) nelerdir?"
            st.rerun()
    with q_col3:
        if st.button("Akademik Hayatı", use_container_width=True):
            st.session_state.quick_prompt = "Murat'ın akademik hayatı ve ODTÜ'deki eğitimi hakkında bilgi verir misin?"
            st.rerun()

prompt = st.chat_input("Mesajınızı yazın...")

if st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None 

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=EMPTY_AVATAR):
        st.markdown(f"<div class='msg-user'>\n\n{prompt}\n\n</div>", unsafe_allow_html=True)

    formatted_history = []
    for i, msg in enumerate(st.session_state.messages[:-1]):
        if i == 0 and msg["role"] == "assistant":
            continue
        role = "model" if msg["role"] == "assistant" else "user"
        formatted_history.append({"role": role, "parts": [msg["content"]]})

    with st.chat_message("assistant", avatar=EMPTY_AVATAR):
        with st.spinner("Asistan yanıtlıyor..."):
            try:
                model = genai.GenerativeModel('gemini-3.0-flash', system_instruction=PERSONAL_INFO)
                chat = model.start_chat(history=formatted_history)
                response = chat.send_message(prompt)
                resp_text = response.text
                
            except Exception as e1:
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=PERSONAL_INFO)
                    chat = model.start_chat(history=formatted_history)
                    response = chat.send_message(prompt)
                    resp_text = response.text
                    
                except Exception as e2:
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=PERSONAL_INFO)
                        chat = model.start_chat(history=formatted_history)
                        response = chat.send_message(prompt)
                        resp_text = response.text
                        
                    except Exception as e3:
                        error_msg = str(e3)
                        if "429" in error_msg or "Quota" in error_msg:
                            resp_text = "Şu an sistemimde yoğunluk var (Google API Kota Limiti). Lütfen yaklaşık 30 saniye bekleyip sorunuzu tekrar sorun."
                        else:
                            resp_text = "Geçici bir bağlantı sorunu oluştu. Lütfen sayfayı yenileyip tekrar deneyin."
        
        st.markdown(f"<div class='msg-assistant'>\n\n{resp_text}\n\n</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": resp_text})
        st.rerun()
