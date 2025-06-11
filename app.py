import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Title
st.title("💘 AI Romantic Poem Generator")
st.write("Let love speak...")

# Language selector
language = st.selectbox("Choose the poem language:", ["English", "Yoruba"])

# Poem topic input
theme = st.text_input("What should the poem be about?", placeholder="e.g. Her eyes, Our journey, Love in Lagos...")

# Load GPT-2
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    return tokenizer, model

tokenizer, model = load_model()

# Generate poem
if st.button("💌 Generate Poem") and theme.strip() != "":
    with st.spinner("Composing a beautiful piece..."):
        prompt = f"Write a romantic poem in {language.lower()} about {theme.strip()}:\n"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.9,
            top_k=50,
            top_p=0.95,
            do_sample=True
        )
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        final_poem = result.replace(prompt.strip(), "").strip()
        st.markdown(f"### 💓 Your Poem\n\n{final_poem}")
