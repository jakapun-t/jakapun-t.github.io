import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from nlp_logic import SAMPLE, analyze_text

st.title("Thai word counter")
text = st.text_area("Reviews", SAMPLE, height=150)
top_n = st.number_input("Top words", min_value=1, max_value=20, value=5)
result = analyze_text(text, top_n=top_n)

st.write("Words:", result["word_count"])
st.write("Unique words:", result["unique_words"])
top = pd.DataFrame(result["top_words"], columns=["word", "count"])
st.dataframe(top)
st.bar_chart(top, x="word", y="count", horizontal=True, sort="-count")
