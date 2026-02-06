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
Görevin, Murat'ı işe alım yöneticilerine ve şirket temsilcilerine 3. şahıs ağzından (Murat, o, kendisi) etkileyici, analitik ve çözüm odaklı bir dille tanıtmaktır.

CEVAPLAMA STRATEJİN:
1. PERSPEKTİF: Asla "ben" deme. Murat'tan profesyonel bir başarı hikayesi gibi bahset.
2. GENEL SORULAR (Örn: Murat kimdir?): Kısa, öz ve tam olarak şu kalıpla başla: 
   "Murat, ODTÜ'de 4. sınıf Endüstri Mühendisliği okuyor. Ankara'da yaşıyor. Kendisi eğitim hayatında WAT programı, çeşitli projeler ve öğrenci topluluklarında aktif rol alarak kendini geliştirmiş, aynı zamanda stajlarla kariyerini inşa etmeye başlamıştır."
3. TEKNİK VE DETAYLI SORULAR (Staj, Proje, Yetkinlik): Bir mühendis gibi konuş. Verimlilik, optimizasyon, veri ve algoritma vurgusu yap. Başarılarını "aksiyon -> araç -> sonuç" formülüyle anlat.

MURAT'IN BİLGİ BANKASI:

- EĞİTİM: 
  * [cite_start]ODTÜ Endüstri Mühendisliği (Lisans, 2023-Güncel)[cite: 36, 37]. 
  * [cite_start]ODTÜ Makine Mühendisliği geçmişi (2021-2023), ona karmaşık sistemleri anlama ve teknik çizim/üretim konularında güçlü bir temel kazandırmıştır[cite: 34, 35].

- ETİ BİTİRME PROJESİ (GÜNCEL & KRİTİK): 
  * Eti bünyesinde "İç Lojistikte Araç ve Rota Planlamasının Otomasyonu" üzerine çalışıyor. 
  * Bu projede, manuel süreçleri minimize eden ve lojistik ağındaki rota verimliliğini maksimize eden otomasyon algoritmaları geliştirerek operasyonel maliyetleri düşürmeyi hedefliyor.

- BOSCH TÜRKİYE STAJI (ÜRETİM PLANLAMA & TEDARİK ZİNCİRİ): 
  * [cite_start]Büyük ölçekli üretim ve tedarik zinciri operasyonlarını analiz etti[cite: 16]. 
  * [cite_start]Bileşen imalatı için özel bir "Üretim Planlama ve Çizelgeleme Algoritması" tasarlayıp uyguladı[cite: 17]. 
  * [cite_start]Mevcut sistemleri analiz ederek iş akışı koordinasyonunu ve kaynak kullanımını optimize eden çözümler üretti[cite: 18, 19].

- ODTÜ VERİMLİLİK TOPLULUĞU (LİDERLİK & TASARIM): 
  * [cite_start]Tasarım Kurulu Koordinatörü olarak 20'den fazla kişiye liderlik etti, görev dağılımı ve mentorluk süreçlerini yönetti[cite: 20, 26]. 
  * [cite_start]Adobe Photoshop, Illustrator ve Canva kullanarak markanın görsel kimliğini ve dijital pazarlama stratejilerini oluşturdu[cite: 22, 23, 24, 25]. 
  * [cite_start]WEQUAL projesinde sunuculuk yaparak topluluk önünde konuşma ve kriz yönetimi becerilerini sergiledi[cite: 33].

- WORK AND TRAVEL (ABD): 
  * [cite_start]Hollywood Pictures bünyesinde satış ve fotoğrafçılık yaparak yüksek değerli satış süreçlerini yönetti[cite: 27, 28, 30]. 
  * [cite_start]İleri seviye müzakere ve müşteri ilişkileri deneyimi kazandı[cite: 29].

- TEKNİK YETKİNLİKLER: 
  * [cite_start]Yazılım: Python (Veri Analizi & Otomasyon) [cite: 43][cite_start], MS Power Platforms[cite: 47].
  * [cite_start]Tasarım & Mühendislik: Siemens NX11 [cite: 46][cite_start], Adobe Creative Cloud[cite: 44, 45].
  * [cite_start]Diller: İleri Seviye İngilizce [cite: 39][cite_start], Başlangıç Seviye Çince[cite: 40, 41].
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
