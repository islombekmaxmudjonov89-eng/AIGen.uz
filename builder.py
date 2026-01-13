import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import time
import json

# Sahifa sozlamalari (Global title)
st.set_page_config(page_title="AIGen.io - Ultimate AI Code Builder", layout="wide", initial_sidebar_state="expanded")

# --- ADMIN PANEL BILAN BOG'LASH ---
def get_ad_link():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data.get("ad_link", "https://rtouchingthewaterw.com/?cGnR=1236571")
    except:
        return "https://rtouchingthewaterw.com/?cGnR=1236571"

SMARTLINK_URL = get_ad_link()

# API Kalit (Ehtiyot bo'l, buni env qilsang yaxshi bo'lardi)
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- CSS DIZAYN (Professional Dark Mode) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    code {{ color: #58a6ff !important; }}
    pre {{ background-color: #161b22 !important; border: 1px solid #30363d; border-radius: 8px; }}
    
    .sidebar-chat {{
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        background-color: #161b22;
        margin-bottom: 10px;
    }}
    div.stButton > button {{
        background-color: #238636 !important;
        color: white !important;
        font-weight: 700 !important;
        width: 100% !important;
        border: none !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #2ea043 !important;
    }}
    .timer-style {{
        color: #ff7b72;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border: 1px solid #f85149;
        border-radius: 10px;
        background: rgba(248, 81, 73, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# Session state
if "generated_html" not in st.session_state:
    st.session_state.generated_html = ""
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# --- SIDEBAR (Inglizcha matnlar) ---
with st.sidebar:
    st.title("🚀 AIGen.io")
    st.caption("AI Code Builder v3.0 (Global Edition)")
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    user_prompt = st.text_area("Describe your app or game:", placeholder="Example: A retro snake game with neon graphics...", height=150)
    
    if st.button("GENERATE CODE ✨"):
        if user_prompt:
            st.session_state.show_download = False 
            
            with st.status("🛠 AI is writing code...", expanded=False):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a professional Full-stack developer. Return only one single HTML file containing all JS/CSS/HTML code. No explanations."},
                            {"role": "user", "content": user_prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    raw_code = completion.choices[0].message.content
                    clean_code = raw_code.replace("```html", "").replace("```javascript", "").replace("```css", "").replace("```", "").strip()
                    st.session_state.generated_html = clean_code
                except Exception as e:
                    st.error(f"Error: API limit reached. Try again in a minute.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    if st.session_state.generated_html:
        if not st.session_state.show_download:
            if st.button("📥 GET SOURCE CODE (FREE)"):
                # Reklama ochish
                js_code = f"window.open('{SMARTLINK_URL}', '_blank');"
                components.html(f"<script>{js_code}</script>", height=0)
                
                placeholder = st.empty()
                for seconds in range(15, 0, -1):
                    placeholder.markdown(f'<div class="timer-style">⚠️ Unlock Code in {seconds}s... (Keep Ad tab open)</div>', unsafe_allow_html=True)
                    time.sleep(1)
                
                placeholder.empty()
                st.session_state.show_download = True
                st.rerun() 
        else:
            st.success("✅ Code Unlocked!")
            st.download_button("📥 DOWNLOAD FILE", st.session_state.generated_html, file_name="AIGen_Code.html", mime="text/html")
            if st.button("Reset 🔄"):
                st.session_state.generated_html = ""
                st.session_state.show_download = False
                st.rerun()

# --- ASOSIY OYNA ---
if st.session_state.generated_html:
    col1, col2 = st.tabs(["👁 PREVIEW", "📜 SOURCE CODE"])
    with col1:
        st.info("Live Preview:")
        components.html(st.session_state.generated_html, height=600, scrolling=True)
    with col2:
        st.info("Full Source Code:")
        st.code(st.session_state.generated_html, language='html')
else:
    st.markdown("<h2 style='text-align: center; color: #8b949e; margin-top: 100px;'>Type your idea and click 'Generate Code' to start!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #484f58;'>Example: 'A landing page for a coffee shop' or 'A simple calculator app'</p>", unsafe_allow_html=True)
