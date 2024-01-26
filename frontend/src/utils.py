import enum
import streamlit as st
import tomllib


def generate_enum(enumClass, enumDict):
    """
    Generates python code for an Enum
    """

    enum_template = """
@unique
class {enumClass}(enum.Enum):
{enumBody}
"""

    enumBody = '\n'.join([f"    {name} = '{value}'" for (name,value) in enumDict.items()])

    return enum_template.format(enumClass=enumClass,enumBody=enumBody)


def streamlit_session_states_init():
    if 'confs' not in st.session_state:
        try:
            #https://docs.python.org/3.11/library/tomllib.html#module-tomllib
            with open("webapp/configs.toml", "rb") as f:
                confs = tomllib.load(f)
                st.session_state.confs = confs
        except Exception as e:
            st.error(e)
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
        st.session_state.show_user_register  = False
        st.session_state.show_user_login  = False
    
    