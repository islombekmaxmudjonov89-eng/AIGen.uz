import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import time
import json
import zipfile
import io

# Sahifa sozlamalari
st.set_page_config(page_title="AIGen.io - Full-Stack AI Builder", layout="wide", initial_sidebar_state="expanded")

# --- ADMIN PANEL BILAN BOG'LASH ---
def get_ad_link():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data.get("ad_link", "https://rtouchingthewaterw.com/?cGnR=1236571")
    except:
        return "https://rtouchingthewaterw.com/?cGnR=1236571"

SMARTLINK_URL = get_ad_link()

# API Kalit (Groq)
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- CSS DIZAYN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .sidebar-chat {{ border: 1px solid #30363d; border-radius: 12px; padding: 15px; background-color: #161b22; margin-bottom: 10px; }}
    div.stButton > button {{ background-color: #238636 !important; color: white !important; font-weight: 700 !important; width: 100% !important; }}
    .timer-style {{ color: #ff7b72; font-weight: bold; text-align: center; padding: 10px; border: 1px solid #f85149; border-radius: 10px; background: rgba(248, 81, 73, 0.1); }}
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
if "generated_html" not in st.session_state: st.session_state.generated_html = ""
if "generated_py" not in st.session_state: st.session_state.generated_py = ""
if "show_download" not in st.session_state: st.session_state.show_download = False

# ZIP yaratish funksiyasi
def create_zip(html, python):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("index.html", html)
        z.writestr("main.py", python)
        z.writestr("requirements.txt", "flask\nflask-cors\nrequests")
    return buf.getvalue()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 AIGen.io PRO")
    st.caption("Full-Stack Builder (Frontend + Backend)")
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    user_prompt = st.text_area("What app should I build?", placeholder="Example: E-commerce with inventory management...", height=150)
    
    if st.button("GENERATE FULL-STACK ✨"):
        if user_prompt:
            st.session_state.show_download = False 
            with st.status("🛠 AI is architecting your App...", expanded=True):
                # PROMPTNI KUCHAYTIRDIK
                system_msg = """You are a Senior Full-stack Developer. 
                Generate a professional web app. 
                1. Use Tailwind CSS for Frontend.
                2. Use Flask for Backend main.py.
                Separate them clearly with: ===BACKEND_START==="""
                
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                raw_res = completion.choices[0].message.content
                
                # Kodlarni ajratish
                if "===BACKEND_START===" in raw_res:
                    parts = raw_res.split("===BACKEND_START===")
                    st.session_state.generated_html = parts[0].replace("```html", "").replace("```", "").strip()
                    st.session_state.generated_py = parts[1].replace("```python", "").replace("```", "").strip()
                else:
                    st.session_state.generated_html = raw_res
                    st.session_state.generated_py = "# No backend generated for this simple task."

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Yuklab olish logikasi (Timer va Reklama bilan)
    if st.session_state.generated_html:
        if not st.session_state.show_download:
            if st.button("📥 UNLOCK FULL PROJECT ZIP"):
                js_code = f"window.open('{SMARTLINK_URL}', '_blank');"
                components.html(f"<script>{js_code}</script>", height=0)
                
                placeholder = st.empty()
                for s in range(15, 0, -1):
                    placeholder.markdown(f'<div class="timer-style">⚠️ Packaging files... {s}s</div>', unsafe_allow_html=True)
                    time.sleep(1)
                
                placeholder.empty()
                st.session_state.show_download = True
                st.rerun() 
        else:
            zip_file = create_zip(st.session_state.generated_html, st.session_state.generated_py)
            st.success("✅ Full Project Ready!")
            st.download_button("📥 DOWNLOAD .ZIP PACK", zip_file, file_name="AIGen_Project.zip", mime="application/zip")

# --- ASOSIY OYNA ---
if st.session_state.generated_html:
    t1, t2, t3 = st.tabs(["👁 PREVIEW", "🌐 HTML/JS", "🐍 PYTHON BACKEND"])
    with t1:
        components.html(st.session_state.generated_html, height=600, scrolling=True)
    with t2:
        st.code(st.session_state.generated_html, language='html')
    with t3:
        st.code(st.session_state.generated_py, language='python')
else:
    st.markdown("<h1 style='text-align: center; margin-top: 150px;'>Build your next $1B Startup in seconds.</h1>", unsafe_allow_html=True)
