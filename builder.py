import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import time
import json
import base64  # Rasmni kodga aylantirish uchun kerak

# Sahifa sozlamalari
st.set_page_config(page_title="AIGen.uz - AI Code Builder", layout="wide", initial_sidebar_state="expanded")

# --- ADMIN PANEL BILAN BOG'LASH ---
def get_ad_link():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data.get("ad_link", "https://rtouchingthewaterw.com/?cGnR=1236571")
    except:
        return "https://rtouchingthewaterw.com/?cGnR=1236571"

SMARTLINK_URL = get_ad_link()

# API Kalit
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- CSS DIZAYN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    code {{ color: #ff79c6 !important; }}
    pre {{ background-color: #161b22 !important; border: 1px solid #30363d; border-radius: 8px; }}
    
    .sidebar-chat {{
        border: 2px solid #4b91ff;
        border-radius: 12px;
        padding: 15px;
        background-color: #0d1117;
        margin-bottom: 10px;
    }}
    .img-box {{
        border: 1px dashed #4b91ff;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        background: #161b22;
    }}
    div.stButton > button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 800 !important;
        width: 100% !important;
    }}
    .timer-style {{
        color: #00ffcc;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border: 1px dashed #00ffcc;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Session state
if "generated_html" not in st.session_state:
    st.session_state.generated_html = ""
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ AIGen.uz")
    st.caption("AI Code Builder v2.1 (Image Support)")
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    user_prompt = st.text_area("Qanday kod yaratamiz?", placeholder="Masalan: Bino Go o'yinini yarat...", height=100)
    
    # RASM YUKLASH QISMI
    st.markdown('<div class="img-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Personaj rasmini yuklang (Ixtiyoriy)", type=['png', 'jpg', 'jpeg'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("KODNI YARATISH ✨"):
        if user_prompt:
            st.session_state.show_download = False 
            
            image_context = ""
            if uploaded_file:
                # Rasmni Base64 ga aylantirish
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode()
                # AI uchun ko'rsatma: Rasmni kodga joylash
                image_context = f"\n\nMUHIM: Mana bu rasmning Base64 kodi: 'data:image/png;base64,{base64_image}'. " \
                                f"Ushbu kodni o'yin personaji (player) uchun src sifatida ishlating. " \
                                f"Hech qanday tashqi link ishlatmang, faqat shu kodni o'yinga joylang."

            with st.status("🛠 AI rasmni o'rganib kod yozmoqda...", expanded=False):
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Siz professional o'yin muhandisisiz. Faqat bitta HTML fayl ichida JS/CSS/HTML kodini qaytaring. Agar rasm kodi berilgan bo'lsa, uni o'yinga to'liq integratsiya qiling."},
                        {"role": "user", "content": user_prompt + image_context}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                raw_code = completion.choices[0].message.content
                clean_code = raw_code.replace("```html", "").replace("```javascript", "").replace("```css", "").replace("```", "").strip()
                st.session_state.generated_html = clean_code
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    if st.session_state.generated_html:
        if not st.session_state.show_download:
            if st.button("📥 GET SOURCE CODE (AD)"):
                js_code = f"window.open('{SMARTLINK_URL}', '_blank');"
                components.html(f"<script>{js_code}</script>", height=0)
                
                placeholder = st.empty()
                for seconds in range(15, 0, -1):
                    placeholder.markdown(f'<div class="timer-style">⚠️ REKLAMANI KO\'RING! {seconds}s...</div>', unsafe_allow_html=True)
                    time.sleep(1)
                
                placeholder.empty()
                st.session_state.show_download = True
                st.rerun() 
        else:
            st.success("✅ Kod tayyor!")
            st.download_button("📥 FAYLNI YUKLAB OLISH", st.session_state.generated_html, file_name="AIGen_Code.html", mime="text/html")
            if st.button("Qayta boshlash 🔄"):
                st.session_state.generated_html = ""
                st.session_state.show_download = False
                st.rerun()

# --- ASOSIY OYNA ---
if st.session_state.generated_html:
    col1, col2 = st.tabs(["👁 PREVIEW", "📜 SOURCE CODE"])
    with col1:
        st.info("Natijani ko'rish:")
        components.html(st.session_state.generated_html, height=600, scrolling=True)
    with col2:
        st.info("Tayyor kod:")
        st.code(st.session_state.generated_html, language='html')
else:
    st.markdown("<h2 style='text-align: center; color: #444;'>Personaj rasmini yuklang va sarguzashtni boshlang!</h2>", unsafe_allow_html=True)
