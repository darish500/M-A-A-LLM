import os
import streamlit as st
import openai
from datetime import datetime

# ——— Page Setup ———
st.set_page_config(
    page_title="💘 Romantic Poem Generator",
    layout="centered",
    page_icon="🌹"
)
st.title("💘 AI Romantic Poem Generator")
st.markdown("Choose language & theme, then let AI craft a poem that speaks to the heart.")

# ——— Load API Key Securely ———
openai.api_key = (
    st.secrets["openai"]["api_key"]
    if "openai" in st.secrets and "api_key" in st.secrets["openai"]
    else os.getenv("OPENAI_API_KEY")
)
if not openai.api_key:
    st.error("🔒 API key not found. Add it to `.streamlit/secrets.toml` or set the `OPENAI_API_KEY` env var.")
    st.stop()

# ——— User Inputs ———
language = st.radio("Poem Language", ["English", "Yorùbá"])
theme = st.text_input("What should the poem be about?", placeholder="e.g. her smile, our journey, moonlight…")
use_gpt4 = st.checkbox("Use GPT-4 (if you have access)", value=False)

# ——— Prompt Builder ———
def build_messages(language, theme):
    system = (
        "You are a world-class romantic poet. "
        "Use vivid metaphors, deep emotion, and heartfelt language."
    )
    if language == "English":
        user = (
            f"Write a deeply emotional romantic poem about “{theme}.” "
            "Use metaphors, longing, vulnerability, and passion—make it unforgettable."
        )
    else:
        user = (
            f"Kọ orin ifẹ̀ pẹ̀lú ìtàn tí yóò kan ọkàn ní Yorùbá nípa “{theme}.” "
            "Lo òwe, ìtàn ìfẹ́, ìbànújẹ, àti ìdúróṣinṣin—jẹ́ kí ó dùn bí àlá alẹ́."
        )
    return [{"role":"system","content":system}, {"role":"user","content":user}]

# ——— Generate & Display ———
if st.button("💌 Generate Poem") and theme.strip():
    with st.spinner("Composing your masterpiece…"):
        model = "gpt-4" if use_gpt4 else "gpt-3.5-turbo"
        messages = build_messages(language, theme.strip())
        resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=250,
        )
        poem = resp.choices[0].message.content.strip()

        st.markdown("### 💓 Your Poem")
        st.text_area("", poem, height=300)

        # ——— Download button ———
        filename = f"poem_{theme.replace(' ','_')}_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        st.download_button(
            "📥 Save as .txt",
            data=poem,
            file_name=filename,
            mime="text/plain"
        )
elif st.button("💌 Generate Poem"):
    st.warning("Please enter a theme first.")
