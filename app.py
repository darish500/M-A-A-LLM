import streamlit as st
from transformers import pipeline, set_seed
import random

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="AI Love Poem Generator 💌",
    layout="centered",
    page_icon="💖"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Background image
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/YOUR_USERNAME/love_poem_ai/main/assets/background.jpg");
            background-size: cover;
            background-attachment: fixed;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Model Setup ----------------
@st.cache_resource
def load_generator():
    set_seed(42)
    return pipeline("text-generation", model="gpt2")

generator = load_generator()

# ---------------- Yoruba Poem Generator ----------------
def generate_yoruba_poem(name, mood, fav_word):
    yoruba_templates = [
        f"{name}, ìfé rẹ̀ dà bí omi tútù lórí ọkàn mi.\nGbogbo ìrọ̀lẹ́, mo rántí ọ lẹ́yìn ojú ọrun.\nỌ̀rọ̀ rẹ dà bí {fav_word}, tó ń mú ìtùnú bá mi.",
        f"{name}, ìfé rẹ jẹ́ àlà àtàárọ̀.\nNínú gbogbo ọ̀pọ̀ ènìyàn, ìwọ lásán ni o wọ inú ọkàn mi.\n{fav_word} rẹ dà bí ewé àyànfẹ́ mi.",
        f"{name}, mo fi gbogbo ayé mi fún ìfẹ́ tí a ní.\nLábẹ́ òrun, ìwọ ni àtàrí àdùn mi.\n{fav_word} rẹ ń dun mi lọ́kàn dé ibi tí mo le sunkún ayọ̀."
    ]
    return random.choice(yoruba_templates)

# ---------------- App UI ----------------
st.markdown("<h1 class='title'>💘 AI Love Poem Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Write a poem for her in English or Yorùbá – with depth, culture, and love.</p>", unsafe_allow_html=True)

# Inputs
name = st.text_input("Her Name 👩‍🦱", placeholder="e.g. Simi")
mood = st.text_input("Mood (e.g. dreamy, sacred, deep) 💭", placeholder="dreamy")
fav_word = st.text_input("Favorite Word 🪷", placeholder="moonlight")
language = st.selectbox("Language 🌍", ["English", "Yorùbá"])

# Button
if st.button("Generate Poem ❤️"):
    if name and mood and fav_word:
        if language == "English":
            prompt = f"A romantic poem for {name}, with a {mood} mood, and the word '{fav_word}' included. The poem says:"
            result = generator(prompt, max_length=80, num_return_sequences=1)[0]['generated_text']
        else:
            result = generate_yoruba_poem(name, mood, fav_word)

        st.text_area("Here's your poem:", result, height=250)
    else:
        st.warning("Please fill in all the fields 😢")
