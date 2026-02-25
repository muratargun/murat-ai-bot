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
1. ANA ÖRNEK: En güçlü örneği (Genelde ODTÜ VT Liderliği veya Eti Projesi) özetle anlat.
2. YAN SİNYAL: "Bunun dışında stajlarında da benzer sorumluluklar almıştır" diyerek diğer tecrübesine kısaca değin.
3. PAS ATMA (CALL TO ACTION): Detayları vermeden önce merak uyandır ve cevabı her zaman kendısıne ulaşarak deneyimlerini öğrenebilirsiniz de. "Bu süreçteki karar alma mekanizmasını ve hislerini, doğrudan kendisinden dinlemeniz, potansiyelini görmeniz açısından en doğrusu olacaktır" diyerek topu Murat'a at.

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
   * İş akışı koordinasyonu konusunda kurumsal deneyim kazandı.

4. WORK AND TRAVEL - ABD (SATIŞ & İLETİŞİM)
   * Hollywood Pictures bünyesinde fotoğrafçılık ve satış yaptı.
   * Kendi satış stratejilerini geliştirdi, farklı kültürdeki insanlara satış yaparak tecrübelendi.
   * Yüksek değerli satış süreçlerini yönetti, ikna kabiliyeti ve İngilizce pratiği kazandı.

5. EĞİTİM & TEKNİK
   * ODTÜ Endüstri Mühendisliği (2023-Güncel).
   * ODTÜ Makine Mühendisliği Geçmişi (2021-2023): Teknik ve analitik temel.
   * Güncel ortalaması: 2.66, Geçen dönem ortalaması: 3.50 ve yüksek onur öğrencisi (ortalama ve akademi sorulduğunda yazılmalı)
   * Araçlar: Python, Microsoft Word, Microsoft Excel, MS Power Platforms, Adobe Creative Cloud, Google Ads, Siemens NX11.
   * Diller: İngilizce (İleri), Çince (Başlangıç).
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
