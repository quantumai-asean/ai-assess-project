import enum
import streamlit as st
import tomllib
import psycopg
from psycopg import errors

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
            with open("frontend/configs.toml", "rb") as f:
                confs = tomllib.load(f)
                st.session_state.confs = confs
        except Exception as e:
            st.error(e)
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
        st.session_state.show_user_register  = False
        st.session_state.show_user_login  = False

        #mode card page
        #st.session_state.modelcard_showassessment = False
        #st.session_state.modelcard_showmodelcard = False

        st.session_state.modelcardpage_states = {'mc_registration_input': None, 
                                                 'mc_modelcard': None, 
                                                 'mc_mctoolkit': None, 
                                                 'sm_RunAssessment': False,
                                                 'sm_showassessment': False,
                                                 'sm_showmodelcard': False
                                                 }




def psql_database_interface(qry:str="", configs: dict = None, action: str = "update"):
    try:
        assert action in {"query","update"}, f"invalid action {action}"
        conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
        q = None
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(qry)
                # Make the changes to the database persistent
                if action == "query":
                    #q = cur.fetchone()
                    q = cur.fetchall()
                else:
                    q = True
            conn.commit()
    except Exception as e:
        print(e)
        return False
    return q

    

    
    