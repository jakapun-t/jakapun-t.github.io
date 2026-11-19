"""The layout examples of lesson 14, card S06. Each value is exactly the code shown in the lesson (after
`import streamlit as st` and `import pandas as pd`); app.py runs one of them, picked by ?ex=<key>, so the
screenshots are real. The word counts come from nlp_logic.analyze_text(SAMPLE): 5 reviews, 25 words, 17 unique,
top words กาแฟ 4, อร่อย 3, ร้าน 2, บรรยากาศ 2, ขนม 2."""

EXAMPLES = {
"stack": '''st.title("Café reviews")
st.write("5 reviews from one café")
st.metric("Reviews", 5)
st.button("Analyze")''',

"sidebar": '''with st.sidebar:
    st.header("Settings")
    top_n = st.slider("Top words", 3, 10, 5)

st.title("Café reviews")
st.write("Showing the top", top_n, "words")''',

"columns": '''st.title("Café reviews")
c1, c2, c3 = st.columns(3)
c1.metric("Reviews", 5)
c2.metric("Words", 25)
c3.metric("Unique words", 17)''',

"tabs": '''top = pd.DataFrame({
    "word": ["กาแฟ", "อร่อย", "ร้าน"],
    "count": [4, 3, 2]})
tab1, tab2 = st.tabs(["Table", "Chart"])
with tab1:
    st.dataframe(top, hide_index=True)
with tab2:
    st.bar_chart(top, x="word", y="count")''',

"expander": '''st.metric("Reviews", 5)
with st.expander("See all 5 reviews"):
    st.write("กาแฟอร่อยมาก ร้านสวย บรรยากาศดี")
    st.write("รอกาแฟนานมาก พนักงานไม่สนใจลูกค้าเลย")
    st.write("ขนมอร่อย แต่กาแฟแพงไปหน่อย")''',

"ratio": '''top = pd.DataFrame({
    "word": ["กาแฟ", "อร่อย", "ร้าน"],
    "count": [4, 3, 2]})
left, right = st.columns([2, 1])
with left:
    st.subheader("Top words")
    st.bar_chart(top, x="word", y="count")
with right:
    st.metric("Reviews", 5)
    st.metric("Words", 25)''',

"cards": '''left, right = st.columns(2)
with left.container(border=True):
    st.subheader("👍 Praise")
    st.write("กาแฟอร่อยมาก ร้านสวย บรรยากาศดี")
with right.container(border=True):
    st.subheader("👎 Complaint")
    st.write("รอกาแฟนานมาก พนักงานไม่สนใจลูกค้าเลย")''',

"wide": '''st.set_page_config(layout="wide")
st.title("Café reviews")
c1, c2, c3 = st.columns(3)
c1.metric("Reviews", 5)
c2.metric("Words", 25)
c3.metric("Unique words", 17)''',

"all": '''st.set_page_config(page_title="Café reviews", layout="wide")

with st.sidebar:
    st.header("Settings")
    top_n = st.slider("Top words", 3, 5, 3)

st.title("Café reviews")
c1, c2, c3 = st.columns(3)
c1.metric("Reviews", 5)
c2.metric("Words", 25)
c3.metric("Unique words", 17)

top = pd.DataFrame({"word": ["กาแฟ", "อร่อย", "ร้าน", "บรรยากาศ", "ขนม"],
                    "count": [4, 3, 2, 2, 2]}).head(top_n)
left, right = st.columns([2, 1])
with left:
    tab1, tab2 = st.tabs(["Chart", "Table"])
    with tab1:
        st.bar_chart(top, x="word", y="count")
    with tab2:
        st.dataframe(top, hide_index=True)
with right.container(border=True):
    st.subheader("Reviews")
    with st.expander("See all 5 reviews"):
        st.write("กาแฟอร่อยมาก ร้านสวย บรรยากาศดี")
        st.write("รอกาแฟนานมาก พนักงานไม่สนใจลูกค้าเลย")''',
}
# variants for the second screenshot of two steps (not shown as code)
EXAMPLES["expander_open"] = EXAMPLES["expander"].replace('st.expander("See all 5 reviews")', 'st.expander("See all 5 reviews", expanded=True)')
EXAMPLES["centered"] = EXAMPLES["wide"].replace('st.set_page_config(layout="wide")\n', '')
