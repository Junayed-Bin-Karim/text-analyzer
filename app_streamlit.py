import streamlit as st
import re
import pandas as pd
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import numpy as np
from datetime import datetime

# ===== Page Config =====
st.set_page_config(
    page_title="Advanced Text Analyzer | Md Junayed Bin Karim",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main { 
        background: radial-gradient(circle at top left, #0f172a 0%, #1e293b 50%, #020617 100%);
        color: #e2e8f0;
    }
    .stApp { background: transparent; }

    .metric-card { 
        background: rgba(15,23,42,0.7); 
        padding: 22px; 
        border-radius: 18px; 
        margin: 15px 0;
        border: 1px solid rgba(96,165,250,0.3);
        box-shadow: 0 4px 25px rgba(37,99,235,0.1);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(96,165,250,0.3);
    }

    .feature-card {
        background: rgba(30,41,59,0.75);
        padding: 16px;
        border-radius: 14px;
        margin: 10px 0;
        border-left: 4px solid #38bdf8;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        background: rgba(56,189,248,0.12);
        border-left-color: #60a5fa;
        transform: scale(1.02);
    }

    .stTextArea>div>div>textarea { 
        background-color: rgba(15,23,42,0.6); 
        color: #f9fafb; 
        border-radius: 14px; 
        padding: 14px; 
        font-size: 16px; 
        border: 1px solid rgba(59,130,246,0.3);
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea:focus {
        outline: none !important;
        border-color: #38bdf8;
        box-shadow: 0 0 12px rgba(56,189,248,0.5);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
        padding: 12px 28px;
        border-radius: 30px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.25s ease;
        width: 100%;
        margin: 12px 0;
        font-weight: 600;
        letter-spacing: 0.4px;
        box-shadow: 0 4px 15px rgba(56,189,248,0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56,189,248,0.5);
    }

    .highlight {
        background: linear-gradient(45deg, #60a5fa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    h1, h2, h3 {
        text-shadow: 0 2px 10px rgba(59,130,246,0.4);
    }
</style>
""", unsafe_allow_html=True)


# ===== Sidebar =====
with st.sidebar:
    st.title("🔧 Settings")
    st.markdown("---")
    
    analysis_options = st.multiselect(
        "Select Analysis Types:",
        ["Basic Statistics", "Text Properties", "Sentiment Analysis", 
         "Word Frequency", "Reading Metrics", "Advanced Features"],
        default=["Basic Statistics", "Text Properties", "Word Frequency"]
    )
    
    show_charts = st.checkbox("Show Interactive Charts", value=True)
    show_raw_data = st.checkbox("Show Raw Data", value=False)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Advanced Text Analyzer** 
    - Word & Character Analysis
    - Sentiment Scoring
    - Reading Level Metrics
    - Visual Analytics
    - Text Transformation
    """)
    st.markdown("---")
    st.markdown("**Developed by:**  \n**Md Junayed Bin Karim**  \nCSE, DIU")

# ===== Header =====
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Advanced Text Analyzer")
    st.markdown("### Comprehensive Text Analysis Tool")
with col2:
    st.markdown(f"<p style='text-align: right; color: #fbbf24;'>🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", 
                unsafe_allow_html=True)

# ===== Text Input =====
text = st.text_area(
    "**Enter your text below:**", 
    height=200,
    placeholder="Type or paste your text here...\n\nExample: The quick brown fox jumps over the lazy dog. This sentence contains all English letters!"
)

# ===== Analysis Functions =====
def calculate_reading_time(text):
    words = len(text.split())
    return max(1, words // 200)  # Assuming 200 words per minute

def calculate_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def calculate_readability(text):
    """Simple readability score (higher = easier to read)"""
    sentences = text.count('.') + text.count('!') + text.count('?')
    words = len(text.split())
    characters = len(text.replace(' ', ''))
    
    if sentences == 0 or words == 0:
        return 50
    
    avg_sentence_length = words / sentences
    avg_word_length = characters / words
    
    readability = 100 - (avg_sentence_length + avg_word_length * 10)
    return max(0, min(100, readability))

def analyze_word_length_distribution(words):
    length_dist = {}
    for word in words:
        length = len(word)
        length_dist[length] = length_dist.get(length, 0) + 1
    return length_dist

# ===== Analyze Button =====
if st.button(" Analyze Text", use_container_width=True):
    if text.strip() == "":
        st.error("⚠️ Please enter some text to analyze!")
    else:
        # ----- Data Cleaning -----
        clean_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        words_list = clean_text.split()
        
        # ----- Basic Stats -----
        lines = [line for line in text.strip().split('\n') if line.strip()]
        total_lines = len(lines)
        vowels = sum(1 for ch in clean_text.lower() if ch in "aeiou")
        consonants = sum(1 for ch in clean_text.lower() if ch.isalpha() and ch not in "aeiou")
        words_count = len(words_list)
        characters = len(clean_text)
        characters_no_space = len(clean_text.replace(' ', ''))
        digits = sum(1 for ch in clean_text if ch.isdigit())
        spaces = clean_text.count(' ')
        specials = len(text) - len(clean_text)
        
        # ----- Advanced Metrics -----
        reading_time = calculate_reading_time(text)
        sentiment, subjectivity = calculate_sentiment(text)
        readability_score = calculate_readability(text)
        
        # ----- Word Analysis -----
        stopwords = {'the','is','and','a','an','to','in','of','for','on','with','as','by','at','be','this','that'}
        filtered_words = [w.lower() for w in words_list if w.lower() not in stopwords and len(w) > 2]
        freq_words = Counter(filtered_words).most_common(10)
        
        # Word length distribution
        word_length_dist = analyze_word_length_distribution(words_list)
        
        # ----- Text Properties -----
        reversed_text = clean_text[::-1]
        is_palindrome = clean_text.replace(" ", "").lower() == reversed_text.replace(" ", "").lower()
        uppercase_count = sum(1 for ch in text if ch.isupper())
        lowercase_count = sum(1 for ch in text if ch.islower())
        
        # ----- Character Frequency -----
        char_freq = Counter(text.lower())
        top_chars = char_freq.most_common(10)
        
        # ----- Display Results -----
        st.markdown("---")
        st.success(" Analysis Complete!")
        
        # ===== Metrics in Columns =====
        if "Basic Statistics" in analysis_options:
            st.markdown("### Basic Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3> {words_count}</h3>
                    <p>Words</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{characters}</h3>
                    <p>Characters</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3> {total_lines}</h3>
                    <p>Lines</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3> {reading_time}m</h3>
                    <p>Reading Time</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ===== Detailed Analysis =====
        col1, col2 = st.columns(2)
        
        with col1:
            if "Text Properties" in analysis_options:
                st.markdown("###  Text Properties")
                st.markdown(f"""
                <div class="feature-card">
                    <strong>Vowels:</strong> <span class="highlight">{vowels}</span>
                </div>
                <div class="feature-card">
                    <strong>Consonants:</strong> <span class="highlight">{consonants}</span>
                </div>
                <div class="feature-card">
                    <strong>Digits:</strong> <span class="highlight">{digits}</span>
                </div>
                <div class="feature-card">
                    <strong>Spaces:</strong> <span class="highlight">{spaces}</span>
                </div>
                <div class="feature-card">
                    <strong>Special Characters:</strong> <span class="highlight">{specials}</span>
                </div>
                <div class="feature-card">
                    <strong>Uppercase Letters:</strong> <span class="highlight">{uppercase_count}</span>
                </div>
                <div class="feature-card">
                    <strong>Lowercase Letters:</strong> <span class="highlight">{lowercase_count}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if "Sentiment Analysis" in analysis_options:
                st.markdown("###  Sentiment Analysis")
                
                sentiment_color = "🟢" if sentiment > 0.1 else "🔴" if sentiment < -0.1 else "🟡"
                subjectivity_level = "High" if subjectivity > 0.6 else "Low" if subjectivity < 0.4 else "Medium"
                
                st.markdown(f"""
                <div class="feature-card">
                    <strong>Sentiment Score:</strong> {sentiment_color} <span class="highlight">{sentiment:.2f}</span>
                    <br><small>{'Positive' if sentiment > 0.1 else 'Negative' if sentiment < -0.1 else 'Neutral'}</small>
                </div>
                <div class="feature-card">
                    <strong>Subjectivity:</strong> <span class="highlight">{subjectivity:.2f}</span>
                    <br><small>{subjectivity_level} subjectivity</small>
                </div>
                <div class="feature-card">
                    <strong>Readability Score:</strong> <span class="highlight">{readability_score:.1f}/100</span>
                    <br><small>{'Easy' if readability_score > 70 else 'Difficult' if readability_score < 30 else 'Moderate'}</small>
                </div>
                <div class="feature-card">
                    <strong>Palindrome:</strong> <span class="highlight">{'✅ Yes' if is_palindrome else '❌ No'}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # ===== Word Frequency =====
        if "Word Frequency" in analysis_options:
            st.markdown("### Word Frequency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top 10 Frequent Words:**")
                for i, (word, count) in enumerate(freq_words, 1):
                    emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"][i-1]
                    st.markdown(f"{emoji} `{word}`: **{count}** occurrences")
            
            with col2:
                if show_charts and freq_words:
                    df_freq = pd.DataFrame(freq_words, columns=['Word', 'Count'])
                    fig = px.bar(df_freq, x='Word', y='Count', 
                                title="Top Words Frequency",
                                color='Count',
                                color_continuous_scale='viridis')
                    st.plotly_chart(fig, use_container_width=True)
        
        # ===== Advanced Features =====
        if "Advanced Features" in analysis_options:
            st.markdown("### ⚡ Advanced Features")
            
            tab1, tab2, tab3 = st.tabs(["📖 Cleaned Text", "🔄 Reversed Text", "📋 Character Analysis"])
            
            with tab1:
                st.text_area("Cleaned Text:", clean_text, height=100)
            
            with tab2:
                st.text_area("Reversed Text:", reversed_text, height=100)
            
            with tab3:
                st.markdown("**Top 10 Most Frequent Characters:**")
                for char, count in top_chars:
                    if char.strip():  # Skip spaces if they're top
                        st.markdown(f"- `{char}`: {count} times")
        
        # ===== Interactive Charts =====
        if show_charts:
            st.markdown("### Visual Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Character distribution chart
                char_data = {
                    'Type': ['Vowels', 'Consonants', 'Digits', 'Spaces', 'Specials'],
                    'Count': [vowels, consonants, digits, spaces, specials]
                }
                df_char = pd.DataFrame(char_data)
                fig1 = px.pie(df_char, values='Count', names='Type', 
                             title="Character Distribution",
                             hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Word length distribution
                if word_length_dist:
                    df_length = pd.DataFrame(list(word_length_dist.items()), 
                                           columns=['Length', 'Count'])
                    fig2 = px.bar(df_length, x='Length', y='Count',
                                 title="Word Length Distribution",
                                 color='Count',
                                 color_continuous_scale='plasma')
                    st.plotly_chart(fig2, use_container_width=True)
        
        # ===== Raw Data =====
        if show_raw_data:
            st.markdown("### 📄 Raw Data")
            data = {
                'Metric': ['Words', 'Characters', 'Lines', 'Vowels', 'Consonants', 
                          'Digits', 'Spaces', 'Special Characters', 'Reading Time (min)'],
                'Value': [words_count, characters, total_lines, vowels, consonants,
                         digits, spaces, specials, reading_time]
            }
            df_raw = pd.DataFrame(data)
            st.dataframe(df_raw, use_container_width=True)

# ===== Footer =====
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #d1d5db;'>"
    "Developed by <strong>Md Junayed Bin Karim</strong> | CSE, DIU | "
    "Advanced Text Analysis Tool</p>", 
    unsafe_allow_html=True
)
