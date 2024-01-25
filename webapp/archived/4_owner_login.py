import streamlit as st
import streamlit_pydantic as sp

from src.schemas import *
import psycopg
from psycopg import errors
from hashlib import blake2s

#experiments on rendering INput Output
st.set_page_config(
    page_title="User Login",
    page_icon="👨🏻‍💼",
)

st.title("Login with your credentials")

PASSWORD_DIGEST_SIZE = 32

with st.form(key="user_form"):
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

        if q[1] == h.hexdigest():
            st.info("Login success!")
        else:
            st.info("Wrong credentials")

        
    except Exception as e:
        st.error(e)