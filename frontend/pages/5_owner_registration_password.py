import streamlit as st
import streamlit.components.v1 as components
# scroll up example: https://discuss.streamlit.io/t/no-way-to-set-focus-at-top-of-screen-on-page-reload-really/15474/14
if "counter" not in st.session_state:
    st.session_state.counter = 1

st.header("Set Focus Here on Page Reload")
st.write("Please click button at bottom of page.")
for x in range(20):
    text_field = st.write("Field "+str(x))

if st.button("Load New Page"):
    st.session_state.counter += 1
#
components.html(
    f"""
        <p>{st.session_state.counter}</p>
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0
)

st.write(f"Page load: {st.session_state.counter}")
   
