import pandas as pd
import streamlit as st
from examples import EXAMPLES

exec(EXAMPLES[st.query_params.get("ex", "stack")], {"st": st, "pd": pd})
