import streamlit as st
import tomllib
from src.utils import *

streamlit_session_states_init()

st.set_page_config(
    page_title="AI Ethics Assessment Homepage",
    page_icon="👋",
)

st.write("# Welcome to AI Ethics Assessment Page! 👋")

#st.sidebar.success("Select a page")

st.markdown(
    """
    Useful Guides for UI
    * [statefull app, useful for multipage](https://docs.streamlit.io/library/advanced-features/session-state)
    * [how to create multi-page app](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)
    * [Page Config](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config)
"""
)

   