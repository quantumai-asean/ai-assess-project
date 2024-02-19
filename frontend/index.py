import streamlit as st
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
    * [pydantic_streamlit src](https://github.com/LukasMasuch/streamlit-pydantic)

    Assessment Guides:
    * [fairlearn in 10 m](https://fairlearn.org/v0.10/quickstart.html#fairlearn-in-10-minutes), [userguide](https://fairlearn.org/v0.10/user_guide/assessment/index.html)
"""
)

   