import streamlit as st
import tomllib

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

#read configs such as database settings and store in session_state
try:
    #https://docs.python.org/3.11/library/tomllib.html#module-tomllib
    with open("webapp/configs.toml", "rb") as f:
        confs = tomllib.load(f)
        if 'confs' not in st.session_state:
            st.session_state.confs = confs
            print(confs)

except Exception as e:
    st.error(e)