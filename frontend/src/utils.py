import enum
import streamlit as st
import toml
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
            #with open("frontend/configs.toml", "rb") as f:
            #    confs = tomllib.load(f)
            #    st.session_state.confs = confs
            st.session_state.confs = toml.load("frontend/configs.toml") 
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
                                                 'sm_showmodelcard': False,
                                                 'sm_registration_page_cnt' : 0
                                                 }



"""
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
"""

def psql_database_interface(qry:str="", configs: dict = None, action: str = "update"):
    assert action in {"query","update"}, f"invalid action {action}"
    q = None
    # first try
    try:
        conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
        conn = psycopg.connect(conn_str)
    except:
        try:
            conn_str = f"host=localhost port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
            conn = psycopg.connect(conn_str)
        except Exception as e:
            print(e)
            return False
    #print(conn_str)
    try:
        cur = conn.cursor()
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
    #print(q)
    return q

#def scroll_to_top():
#    js = '''
#    <script>
#        var body = window.parent.document.querySelector(".main");
#        console.log(body);
#        body.scrollTop = 0;
#    </script>
#    '''
#    st.components.v1.html(js)

def scroll_to_top(var):
    st.components.v1.html(
        f"""
            <p>{var}</p>
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
        """,
        height=0
    )


        




    
    