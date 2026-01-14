import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import time
import json
import zipfile
import io

# 1. Sahifa sozlamalari
st.set_page_config(page_title="AIGen.io - Professional Full-Stack AI", layout="wide", initial_sidebar_state="expanded")

# --- ADMIN PANEL (REKLAMA) ---
def get_ad_link():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data.get("ad_link", "https://rtouchingthewaterw.com/?cGnR=1236571")
    except:
        return "https://rtouchingthewaterw.com/?cGnR=1236571"

SMARTLINK_URL = get_ad_link()

# --- API SOZLAMALARI ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- CSS DIZAYN (Premium Dark Mode) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .sidebar-chat {{ border: 1px solid #30363d; border-radius: 12px; padding: 15px; background-color: #161b22; margin-bottom: 10px; }}
    div.stButton > button {{ background-color: #238636 !important; color: white !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; transition: 0.3s; }}
    div.stButton > button:hover {{ background-color: #2ea043 !important; transform: scale(1.02); }}
    .timer-style {{ color: #ff7b72; font-weight: bold; text-align: center; padding: 15px; border: 1px solid #f85149; border-radius: 10px; background: rgba(248, 81, 73, 0.1); margin-top: 10px; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ color: #8b949e; }}
    .stTabs [aria-selected="true"] {{ color: #58a6ff !important; border-bottom-color: #58a6ff !important; }}
    </style>
    """, unsafe_allow_html=True)

# Session State (Ma'lumotlarni eslab qolish uchun)
if "gen_html" not in st.session_state: st.session_state.gen_html = ""
if "gen_py" not in st.session_state: st.session_state.gen_py = ""
if "show_dl" not in st.session_state: st.session_state.show_dl = False

# ZIP yaratish funksiyasi
def create_project_zip(html, python):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("index.html", html)
        z.writestr("main.py", python)
        z.writestr("requirements.txt", "flask\nflask-cors\nrequests")
    return buf.getvalue()

# --- SIDEBAR (Boshqaruv Paneli) ---
with st.sidebar:
    st.title("🚀 AIGen.io PRO")
    st.caption("Full-Stack Engine v4.0")
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    user_prompt = st.text_area("Describe your full-stack app:", placeholder="Example: A login system that stores user data...", height=150)
    
    if st.button("GENERATE FULL PROJECT ✨"):
        if user_prompt:
            st.session_state.show_dl = False 
            with st.status("🛠 Building Frontend & Backend...", expanded=True):
                # MEGA PROMPT: Ikkala faylni bir-biriga zanjirdek bog'laymiz
                system_instruction = """You are a Senior Full-stack Developer. 
                Generate TWO connected files:
                1. index.html: Professional UI with Tailwind CSS. Every button/form must use JS fetch() to call the backend.
                2. main.py: A Flask backend that has routes (@app.route) for EVERY interactive element in the HTML.
                The backend must handle logic for all buttons created. 
                Separate them with this exact marker: ===BACKEND_CODE_START==="""
                
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    full_response = completion.choices[0].message.content
                    
                    if "===BACKEND_CODE_START===" in full_response:
                        parts = full_response.split("===BACKEND_CODE_START===")
                        st.session_state.gen_html = parts[0].replace("```html", "").replace("```", "").strip()
                        st.session_state.gen_py = parts[1].replace("```python", "").replace("```", "").strip()
                    else:
                        st.session_state.gen_html = full_response
                        st.session_state.gen_py = "# Backend logic could not be generated. Please try a more specific prompt."
                except Exception as e:
                    st.error("API Limit reached. Wait a moment.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Yuklab olish (Reklama va Timer bilan)
    if st.session_state.gen_html:
        if not st.session_state.show_dl:
            if st.button("📥 GET FULL-STACK ZIP"):
                # Reklama ochish
                js_script = f"window.open('{SMARTLINK_URL}', '_blank');"
                components.html(f"<script>{js_script}</script>", height=0)
                
                timer_place = st.empty()
                for i in range(15, 0, -1):
                    timer_place.markdown(f'<div class="timer-style">⚠️ Unlocking Project Files... {i}s</div>', unsafe_allow_html=True)
                    time.sleep(1)
                
                timer_place.empty()
                st.session_state.show_dl = True
                st.rerun()
        else:
            zip_data = create_project_zip(st.session_state.gen_html, st.session_state.gen_py)
            st.success("✅ Project Ready!")
            st.download_button("📥 DOWNLOAD PROJECT (.ZIP)", zip_data, file_name="AIGen_FullStack.zip", mime="application/zip")
            if st.button("Reset 🔄"):
                st.session_state.gen_html = ""
                st.session_state.gen_py = ""
                st.session_state.show_dl = False
                st.rerun()

# --- ASOSIY EKRAN ---
if st.session_state.gen_html:
    tab1, tab2, tab3 = st.tabs(["👁 PREVIEW", "📜 INDEX.HTML", "🐍 MAIN.PY (BACKEND)"])
    
    with tab1:
        st.info("Live Preview (Frontend only):")
        components.html(st.session_state.gen_html, height=600, scrolling=True)
    
    with tab2:
        st.code(st.session_state.gen_html, language="html")
        
    with tab3:
        st.markdown("### Backend Logic (Python Flask)")
        st.info("This code handles all the buttons and forms in your HTML.")
        st.code(st.session_state.gen_py, language="python")
else:
    st.markdown("<h1 style='text-align: center; margin-top: 100px; color: #58a6ff;'>AIGen.io PRO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8b949e;'>Build fully functional Apps with Python Backends in seconds.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #484f58;'>Example: 'A bank app where I can send money and see my balance'</p>", unsafe_allow_html=True)
