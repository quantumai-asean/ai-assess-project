import streamlit as st
from pydantic import BaseModel

import streamlit_pydantic as sp


class ExampleModel(BaseModel):
    some_text: str
    some_number: int = 10  # Optional
    some_boolean: bool = True  # Option


st.title("Test Model Card")

input_data = sp.pydantic_input("model_input", ExampleModel, "no") #"sidebar")