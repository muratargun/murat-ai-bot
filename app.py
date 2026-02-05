import streamlit as st
import google.generativeai as genai

st.title("🛠️ Sistem Teşhis Ekranı")

# 1. API Anahtarını Kontrol Et
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # Güvenlik için sadece ilk ve son 4 karakteri gösterelim
    masked_key = f"{api_key[:4]}...{api_key[-4:]}"
    st.success(f"✅ API Anahtarı Secrets içinde bulundu: {masked_key}")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ API Anahtarı Secrets'tan okunamadı! Hata: {e}")
    st.stop()

# 2. Modelleri Listele (Anahtarın neleri gördüğünü test et)
st.write("---")
st.write("📡 Google Sunucularına Bağlanılıyor...")

try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    
    if available_models:
        st.success(f"✅ Bağlantı Başarılı! Anahtarınız şu {len(available_models)} modeli görebiliyor:")
        st.code("\n".join(available_models))
        st.info("Eğer bu listeyi görüyorsanız, anahtarınız SAĞLAM demektir.")
    else:
        st.warning("⚠️ Bağlantı kuruldu ama hiç model bulunamadı. Anahtarınızın yetkisi kısıtlı olabilir.")

except Exception as e:
    st.error("❌ BAĞLANTI HATASI (Sorun Burada!)")
    st.error(f"Hata Mesajı: {e}")
    st.write("### Olası Çözümler:")
    st.markdown("""
    1. **Anahtar Hatalı:** Secrets kısmında anahtarı tırnak içinde yanlış yazmış olabilirsiniz. 
       - Yanlış: `GEMINI_API_KEY = ""AIza...""` (Çift tırnak içinde çift tırnak)
       - Doğru: `GEMINI_API_KEY = "AIza..."`
    2. **Kopyalama Hatası:** Anahtarın başında veya sonunda boşluk kalmış olabilir.
    3. **Proje Silinmiş:** Google AI Studio'da anahtarı oluşturduğunuz proje silinmiş olabilir.
    """)
