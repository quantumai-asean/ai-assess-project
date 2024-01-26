import streamlit as st
import streamlit_pydantic as sp

from src.schemas import *
import psycopg
from psycopg import errors
from hashlib import blake2s
from src.enums import EnumCountry 


#experiments on rendering INput Output
st.set_page_config(
    page_title="User Registration With Password",
    page_icon="👨🏻‍💼",
)

def input_validation (input_model) -> bool:
    PASSWORD_CONSTRAINT = 8
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
    PASSWORD_DIGEST_SIZE = 32
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
    except errors.UniqueViolation as e:
        st.error("Record with same Name or Email already exists.")


st.title("Register as a User")

with st.form(key="user_regform"):
    input_model = sp.pydantic_input(key="user_registration", model=pydUserRegistrationInput, group_optional_fields="no")
    submit_registration = st.form_submit_button(label="submit")

if submit_registration:
    #st.write(input_model)
    #check password
    if input_validation(input_model):
        insert_userregistration_database(input_model)
 
