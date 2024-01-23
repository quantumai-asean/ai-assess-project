import streamlit as st
import streamlit_pydantic as sp

from src.schemas import *
import psycopg
from psycopg import errors

#experiments on rendering INput Output
st.set_page_config(
    page_title="User Registration",
    page_icon="👨🏻‍💼",
)

st.title("Register as a Assessment User")

with st.form(key="user_form"):
    input_model = sp.pydantic_input(key="user_input_model", model=pydOwner, group_optional_fields="no")
    submit = st.form_submit_button(label="submit")

if submit:
    try:
        update_owner_str = f"INSERT INTO owner (name,contact) VALUES ('{input_model['name']}', '{input_model['contact']}');"
        with psycopg.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres password=postgres") as conn:
            with conn.cursor() as cur:
                cur.execute(update_owner_str)
                # Make the changes to the database persistent
            conn.commit()
        st.write("Success!")
    except errors.UniqueViolation as e:
        st.write("Record with same Name already exists in record.")