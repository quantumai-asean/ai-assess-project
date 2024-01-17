import streamlit as st
from pydantic import BaseModel, Field
import datetime
import streamlit_pydantic as sp

#experiments on rendering INput Output
st.set_page_config(
    page_title="Input Output Rendering Test",
    page_icon="🚀",
)


st.title("Input Output")


class ExampleRenderOutputModel(BaseModel):
    text: str = Field(..., description="A text property")
    integer: int = Field(..., description="An integer property.")


class ExampleRenderInputModel(BaseModel):
    text_input: str = "ChangeME"
    integer_input: int = 100  # Optional
    #some_boolean: bool = True  # Option

#input_data = sp.pydantic_input("model_input", ExampleRenderInputModel, "sidebar")  

# batch input https://blog.streamlit.io/introducing-submit-button-and-forms/
with st.form(key="pydantic_form"):
    #sp.pydantic_input(key="my_input_model", model=ExampleRenderInputModel)
    output_instance = ExampleRenderOutputModel(text="ChangeMe", integer=100)
    input_model = sp.pydantic_input(key="my_input_model", model=ExampleRenderInputModel)
    submit = st.form_submit_button(label="update")

if submit:
    output_instance.text = input_model['text_input']
    output_instance.integer = input_model['integer_input']
    sp.pydantic_output(output_instance)
    




