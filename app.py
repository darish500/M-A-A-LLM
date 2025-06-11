import streamlit as st
from transformers import pipeline
from datetime import datetime

# Load the model (emotional & expressive)
@st.cache_resource
def load_model():
    # Use GPT-Neo for better emotional depth
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
    return generator

# Build the poem prompt
def build_prompt(language, theme):
    if language == "English":
        return f"Write a deeply emotional romantic poem about {theme}. Use metaphors, longing, and vulnerability. Make the reader feel loved."
    else:
        return f"Kọ orin ifẹ̀ pẹ̀lú ìtàn àyà tó kún fún ìfẹ́ àti ìbànújẹ nípa {theme}. Ṣe é kún fún òwe, ìtàn ayé àti àkúnya."

# Generate the poem
def generate_poem(generator, prompt):
    result = generator(prompt, max_length=200, num_return_sequences=1)
    return result[0]['generated_text']

# Save poem to file
def save_poem(poem, theme, language):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"poem_{theme}_{language}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(poem)
    return filename

# Streamlit UI
st.set_page_config(page_title="Love Poem Generator ❤️", layout="centered")
st.title("💌 Romantic Poem Generator")
st.markdown("Let your feelings speak... in English or Yoruba.")

# User inputs
language = st.radio("Choose your language:", ("English", "Yoruba"))
theme = st.text_input("What should the poem be about? (e.g., her smile, our love, distance)")

if st.button("Generate Poem"):
    if theme.strip() == "":
        st.warning("Please enter a theme for your poem.")
    else:
        with st.spinner("Crafting your poem... 💘"):
            generator = load_model()
            prompt = build_prompt(language, theme)
            poem = generate_poem(generator, prompt)
            st.success("Done! Here's your love poem:")
            st.text_area("Poem", poem, height=300)

            if st.button("💾 Save Poem"):
                file = save_poem(poem, theme, language)
                st.success(f"Poem saved as '{file}'")

