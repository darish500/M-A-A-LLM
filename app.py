import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime

# Load model (better than GPT-2)
@st.cache_resource
def load_model():
    model_name = "EleutherAI/gpt-neo-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# UI
st.title("💖 AI Poem Generator (Powered by GPT-Neo)")
prompt = st.text_area("Enter a topic, feeling, or first line:", "Her eyes sparkled like...")

max_len = st.slider("Max Poem Length", 30, 30000, 120)
temperature = st.slider("Creativity (Temperature)", 0.7, 1.5, 1.0)

if st.button("Generate Poem 🎤"):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=max_len,
        do_sample=True,
        temperature=temperature,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.2,
        pad_token_id=tokenizer.eos_token_id
    )
    poem = tokenizer.decode(output[0], skip_special_tokens=True)
    st.subheader("🌺 Your Generated Poem")
    st.write(poem)

    if st.button("💾 Save Poem"):
        filename = f"poem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(poem)
        st.success(f"Poem saved as {filename}")
