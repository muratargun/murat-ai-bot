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

# --- ÜST BAR (CV İNDİRME VE TEMA SEÇİMİ) ---
col1, col2, col3 = st.columns([0.65, 0.20, 0.15])

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
            data=b"CV dosyasi bulunamadi. Lutfen GitHub deposuna 'Murat Argun Resume.pdf' dosyasini yukleyin.",
            file_name="hata_raporu.txt",
            use_container_width=True
        )

with col3:
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
    title_color = "#111827"
    btn_bg = "#FFFFFF"
    btn_text = "#111827"

# --- CSS: TASARIM, BAŞLIK VE BUTONLAR ---
st.markdown(f"""
    <style>
    header, #MainMenu, footer {{visibility: hidden;}}

    .new-pro-title {{
        position: fixed; 
        top: 20px;
        left: 25px;
        z-index: 999; 
    }}
    .title-name {{
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem; 
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

    @media (max-width: 600px) {{
        .new-pro-title {{top: 15px; left: 15px;}}
        .title-name {{font-size: 1rem;}}
        .title-role {{font-size: 0.85rem;}}
    }}

    div[data-baseweb="select"] > div {{
        background-color: {select_bg} !important;
        color: {text_color} !important; 
        border: 1px solid {border_color} !important;
    }}
    li[role="option"] {{ color: {text_color} !important; }}

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
        border-
