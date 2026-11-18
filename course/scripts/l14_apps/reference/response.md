```python
import pandas as pd
import streamlit as st
from nlp_logic import SAMPLE, analyze_text

st.set_page_config(
    page_title="Café Review Insights",
    page_icon="☕",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF9F6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("### ☕ Café Review Insights")
st.markdown("*what customers talk about most*")

# Expandable reviews input box
with st.expander("▶ Paste reviews (click to open)"):
    text = st.text_area("Reviews", SAMPLE, height=150, label_visibility="collapsed")

result = analyze_text(text)

# Metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📝 Reviews", result.get("review_count", 1))
with col2:
    st.metric("abc Words", result["word_count"])
with col3:
    st.metric("✨ Unique words", result["unique_words"])

# Chart and Table tabs
tab_chart, tab_table = st.tabs(["Chart", "Table"])

top = pd.DataFrame(result["top_words"], columns=["word", "count"])

with tab_chart:
    st.bar_chart(top, x="word", y="count", horizontal=True, sort="-count")

with tab_table:
    st.dataframe(top, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>made with Streamlit</p>",
    unsafe_allow_html=True,
)
```