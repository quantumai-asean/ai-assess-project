import streamlit as st


st.set_page_config(
    page_title="AI Ethics Assessment Homepage",
    page_icon="👋",
)

st.write("# Welcome to AI Ethics Assessment Page! 👋")

st.sidebar.success("Select a page")

st.markdown(
    """
    Useful Guides for UI
    * remember that streamlit is stateless
    * [how to create multi-page app](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)
    * [Page Config](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config)
"""
)