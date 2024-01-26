import streamlit as st
import streamlit_pydantic as sp

from src.schemas import *
import psycopg
from psycopg import errors
from hashlib import blake2s
from src.enums import EnumCountry 
from src.utils import *

streamlit_session_states_init()

#experiments on rendering INput Output
st.set_page_config(
    page_title="User Management",
    page_icon="👨🏻‍💼",
)


PASSWORD_DIGEST_SIZE = 32
PASSWORD_CONSTRAINT = 8

def show_login():  
    with st.form(key="user_login_form"):
        input_model = sp.pydantic_input(key="user_login_model", model=pydUserLogin, group_optional_fields="no")
        submit = st.form_submit_button(label="submit")

    if submit:
        
        try:
            login_user_query = f"SELECT id, password FROM userlogin WHERE email = '{input_model['email']}'"
            #with psycopg.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres password=postgres") as conn:
            configs = st.session_state.confs['database']['server']
            conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
            with psycopg.connect(conn_str) as conn:
                with conn.cursor() as cur:
                    cur.execute(login_user_query)
                    q = cur.fetchone()
                    # Make the changes to the database persistent

            h = blake2s(digest_size=PASSWORD_DIGEST_SIZE)
            h.update(input_model['password'].encode())

            if q:
                if q[1] == h.hexdigest():
                    st.info("Login success!")
                    st.session_state.user_logged_in = True
                    st.rerun()
                    #st.switch_page("pages/2_model_management.py")
                else:
                    st.warning("Wrong credentials")
            else:
                st.warning("Wrong credentials")
        except Exception as e:
            st.error(e)
    if st.button("No profile yet? Create one"):
        st.session_state.show_user_login = False
        st.session_state.show_user_register = True
        st.session_state.user_logged_in = False
        st.rerun()



def input_validation (input_model) -> bool:   
    if input_model['create_password'] == "":
        st.warning("Password must not be empty")
        return False
    elif len(input_model['create_password']) < PASSWORD_CONSTRAINT:
        st.warning(f"Password too short, must be longer than {PASSWORD_CONSTRAINT} chars.")
        return False
    elif input_model['create_password'] != input_model['confirm_password']:
        st.warning("Password mismatch!")
        return False
    elif input_model['name'] == "":
        st.warning("Name must not be empty")
        return False
    elif input_model['email'] == "":
        st.warning("Email must not be empty")
        return False
    else:
        return True 
    
def insert_userregistration_database(input_model):
    try:
        h = blake2s(digest_size=PASSWORD_DIGEST_SIZE)
        h.update(input_model['create_password'].encode())
        update_owner_str = f"""INSERT INTO userlogin (name, email, url, country, password) 
                            VALUES ( '{input_model['name']}', '{input_model['email'].lower()}', '{input_model['url']}',  
                            '{EnumCountry(input_model['country']).name}',  '{h.hexdigest()}' ) 
                            ;"""
        #with psycopg.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres password=postgres") as conn:
        configs = st.session_state.confs['database']['server']
        conn_str = f"host={configs['host']} port={configs['port']} dbname={configs['dbname']} user={configs['user']} password={configs['password']}"
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(update_owner_str)
                # Make the changes to the database persistent
            conn.commit()
        st.info("Success!")
        st.session_state.show_user_login = True
        st.session_state.show_user_register = False
        st.session_state.user_logged_in = False
        st.rerun()
    except errors.UniqueViolation as e:
        st.error("Record with same Name or Email already exists.")



def show_create():    
    with st.form(key="user_regform"):
        input_model = sp.pydantic_input(key="user_registration", model=pydUserRegistrationInput, group_optional_fields="no")
        submit_registration = st.form_submit_button(label="submit")

    if submit_registration:
        #st.write(input_model)
        #check password
        if input_validation(input_model):
            insert_userregistration_database(input_model)
    if st.button("Login as Registered User"):
        st.session_state.show_user_login = True
        st.session_state.show_user_register = False
        st.session_state.user_logged_in = False
        st.rerun()


def show_ModelOwnerView():
    if st.button("Logout"):
        st.session_state.user_logged_in = False
        st.session_state.show_user_login = False
        st.session_state.show_user_register = False
        st.rerun()


def show_noop():
    pass

show_function = show_noop

if st.session_state.user_logged_in:
    # display user's data and user's Model's card
    page_title = "Your Model Cards"
    show_function = show_ModelOwnerView
    show_button = False
elif st.session_state.show_user_login:
    page_title = "Login with your credentials"
    show_function = show_login
    show_button = False
elif st.session_state.show_user_register:
    page_title = "Create A Model Owner's Profile"
    show_function = show_create
    show_button = False
else:
    page_title = "Login or Create a Profile"
    show_button = True


st.title(page_title)

show_function()



if show_button:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.show_user_login = True
            st.rerun() #! not the optimum way to refresh
    with col2:
        if st.button("Create Profile"):
            st.session_state.show_user_register = True
            st.rerun() #! not the optimum way to refresh 

    

 
