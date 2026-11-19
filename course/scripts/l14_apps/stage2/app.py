import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from nlp_logic import SAMPLE, analyze_text

st.title("Thai word counter")

# 1. the settings go in the sidebar
with st.sidebar:
    st.header("Settings")
    top_n = st.number_input("Top words", min_value=1, max_value=20, value=5)

text = st.text_area("Reviews", SAMPLE, height=150)
result = analyze_text(text, top_n=top_n)

# 2. three metric cards side by side
c1, c2, c3 = st.columns(3)
c1.metric("Reviews", result["lines"])
c2.metric("Words", result["word_count"])
c3.metric("Unique words", result["unique_words"])

# 3. table on the left, chart on the right
left, right = st.columns(2)
top = pd.DataFrame(result["top_words"], columns=["word", "count"])
with left:
    st.subheader("Top words")
    st.dataframe(top, hide_index=True)
with right:
    st.subheader("Word frequency")
    st.bar_chart(top, x="word", y="count", horizontal=True, sort="-count")
