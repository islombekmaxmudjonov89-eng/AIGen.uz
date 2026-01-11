import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import time
import json # config.json ni o'qish uchun kerak

# Sahifa sozlamalari
st.set_page_config(page_title="AIGen.uz - AI Code Builder", layout="wide", initial_sidebar_state="expanded")

# --- ADMIN PANEL BILAN BOG'LASH ---
def get_ad_link():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data.get("ad_link", "https://rtouchingthewaterw.com/?cGnR=1236571")
    except:
        # Agar faylda xato bo'lsa, zaxira link
        return "https://rtouchingthewaterw.com/?cGnR=1236571"

SMARTLINK_URL = get_ad_link()

# API Kalit
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- CSS DIZAYN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    header {{ visibility: hidden; }}
    .block-container {{ padding: 0rem; }}
    [data-testid="stSidebar"] {{ background-color: #161b22 !important; border-right: 1px solid #30363d; }}
    
    .sidebar-chat {{
        border: 2px solid #ff4b4b;
        border-radius: 12px;
        padding: 15px;
        background-color: #0d1117;
        margin: 10px;
    }}

    /* Tugmalar */
    div.stButton > button, div.stDownloadButton > button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
        height: 45px !important;
        width: 100% !important;
        text-transform: uppercase;
    }}
    
    .timer-style {{
        color: #00ffcc;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border: 1px dashed #00ffcc;
        border-radius: 10px;
    }}

    iframe {{ border: none; background-color: white; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Session state
if "generated_html" not in st.session_state:
    st.session_state.generated_html = "<html><body style='background:#1a1a1a; display:flex; justify-content:center; align-items:center; height:100vh; color:#444;'><h1>AIGen.uz Preview Area</h1></body></html>"
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ AIGen.uz")
    st.caption("AI Code Builder v2.0")
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    user_prompt = st.text_area("Prompt", placeholder="Qanday kod yaratamiz?", height=200, label_visibility="collapsed")
    
    if st.button("KODNI YARATISH ✨"):
        if user_prompt:
            st.session_state.show_download = False 
            with st.status("🛠 Kod yozilmoqda...", expanded=False):
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Siz web-muhandissiz. To'liq HTML kod qaytaring."},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.session_state.generated_html = completion.choices[0].message.content.replace("```html", "").replace("```", "").strip()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    if not st.session_state.show_download:
        if st.button("📥 GET SOURCE CODE (AD)"):
            # Reklamani ochish
            js_code = f"window.open('{SMARTLINK_URL}', '_blank');"
            components.html(f"<script>{js_code}</script>", height=0)
            
            # 30 soniyali taymer
            placeholder = st.empty()
            progress_bar = st.progress(0)
            
            for seconds in range(30, 0, -1):
                placeholder.markdown(f'<div class="timer-style">⚠️ REKLAMANI KO\'RING! {seconds}s qoldi...</div>', unsafe_allow_html=True)
                progress_bar.progress((30 - seconds + 1) / 30)
                time.sleep(1)
            
            placeholder.empty()
            progress_bar.empty()
            st.session_state.show_download = True
            st.rerun() 
    else:
        st.success("✅ Rahmat! Kod tayyor.")
        st.download_button("📥 FAYLNI YUKLAB OLISH", st.session_state.generated_html, file_name="AIGen_Code.html", mime="text/html")
        if st.button("Qayta boshlash 🔄"):
            st.session_state.show_download = False
            st.rerun()

# --- ASOSIY OYNA ---
components.html(st.session_state.generated_html, height=1000, scrolling=True)
