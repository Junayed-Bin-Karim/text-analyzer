import streamlit as st
import re
import pandas as pd
from collections import Counter

# ===== Page Config =====
st.set_page_config(
    page_title="Advanced Text Analyzer | Md Junayed Bin Karim",
    layout="centered",
)

# ===== Custom CSS =====
st.markdown("""
<style>
body { background: linear-gradient(135deg, #3b82f6, #9333ea); color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
textarea, .stTextArea>div>div>textarea { background-color: rgba(255,255,255,0.1); color:white; border-radius:10px; padding:10px; font-size:16px; width:100%;}
div.stButton > button { background-color:#10b981; color:white; padding:10px 25px; border-radius:10px; font-size:16px; border:none; cursor:pointer; transition: all 0.3s ease;}
div.stButton > button:hover { background-color:#059669; transform: scale(1.05);}
.stMarkdown { background: rgba(255,255,255,0.15); padding:20px; border-radius:15px; margin-top:15px;}
</style>
""", unsafe_allow_html=True)

# ===== Header =====
st.title("Advanced Text Analyzer")
st.subheader("Developed by Md Junayed Bin Karim | CSE, DIU")

# ===== Text Input =====
text = st.text_area("Type or paste your text here (multi-line supported):", height=150)

# ===== Analyze Button =====
if st.button("Analyze Text"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        # ----- Data Cleaning -----
        clean_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        # ----- Basic Stats -----
        lines = text.strip().split('\n')
        total_lines = len(lines)
        vowels = sum(1 for ch in clean_text.lower() if ch in "aeiou")
        consonants = sum(1 for ch in clean_text.lower() if ch.isalpha() and ch not in "aeiou")
        words = len(clean_text.split())
        characters = len(clean_text)
        digits = sum(1 for ch in clean_text if ch.isdigit())
        specials = len(text) - len(clean_text)

        # ----- Most Frequent Words -----
        stopwords = {'the','is','and','a','an','to','in','of','for','on','with','as','by'}
        word_list = [w.lower() for w in clean_text.split() if w.lower() not in stopwords]
        freq_words = Counter(word_list).most_common(5)

        # ----- Reverse & Palindrome -----
        reversed_text = clean_text[::-1]
        is_palindrome = clean_text.replace(" ", "").lower() == reversed_text.replace(" ", "").lower()

        # ----- Display Results -----
        st.success("Analysis Result")
        st.markdown(f"**Total Lines:** {total_lines}")
        st.markdown(f"**Total Words:** {words}")
        st.markdown(f"**Vowels:** {vowels}")
        st.markdown(f"**Consonants:** {consonants}")
        st.markdown(f"**Digits:** {digits}")
        st.markdown(f"**Special Characters:** {specials}")
        st.markdown(f"**Cleaned Text:** {clean_text}")
        st.markdown(f"**Reversed Text:** {reversed_text}")
        st.markdown(f"**Palindrome?:** {'Yes' if is_palindrome else '❌ No'}")

        st.markdown("**Top 5 Frequent Words:**")
        for word, count in freq_words:
            st.markdown(f"- {word} : {count}")

        # ----- Charts -----
        st.bar_chart({"Vowels": vowels, "Consonants": consonants, "Digits": digits, "Specials": specials})
