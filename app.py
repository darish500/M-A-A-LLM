import openai
import streamlit as st
from datetime import datetime

# Set your API key directly (temporary for testing, remove later)
openai.api_key = "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"

st.set_page_config(page_title="Poem Generator", layout="centered")
st.title("📝 Emotional Poem Generator (Yorùbá + English)")

# Text input for feelings
feeling = st.text_input("Tell me what's on your heart (in English or Yorùbá)")

# Generate button
if st.button("Generate Poem"):
    if feeling.strip() == "":
        st.warning("Please enter something you're feeling.")
    else:
        with st.spinner("Composing your heartfelt poem..."):
            messages = [
                {"role": "system", "content": "You're a heartfelt poet that writes emotional, beautiful poems in both English and Yorùbá, starting with Yorùbá then translating to English."},
                {"role": "user", "content": f"Write a deep, emotional poem about: {feeling}"}
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                poem = response['choices'][0]['message']['content']
                st.text_area("Your Poem ❤️", poem, height=400)

                # Save poem to file
                file_name = f"poem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                st.download_button("📥 Download Poem", poem, file_name, "text/plain")
            except Exception as e:
                st.error(f"Error: {str(e)}")
