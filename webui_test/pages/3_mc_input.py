import streamlit as st
#from pydantic import BaseModel, Field, StringConstraints, ConfigDict
#import datetime
import streamlit_pydantic as sp
#import model_card_toolkit as mctlib
#from typing_extensions import Annotated

#experimental modules
#import dataclasses
#from typing import Any, Dict, List, Optional, Union
#from model_card_toolkit.model_card import (
#    Citation, ConfidenceInterval, Considerations, Dataset, Graphic,
#    GraphicsCollection, KeyVal, License, Limitation, ModelCard, ModelDetails,
#    ModelParameters, Owner, PerformanceMetric, QuantitativeAnalysis, Reference,
#    Risk, SensitiveData, Tradeoff, UseCase, User, Version, load_model_card
#)


from src.schemas import *



#experiments on rendering INput Output
st.set_page_config(
    page_title="Registering a Model Card",
    page_icon="🚀",
)


st.title("Registering A Model Card")



#or idea: https://github.com/LukasMasuch/streamlit-pydantic/blob/390a45aba7bf8caccc297c335715cc141db490af/src/streamlit_pydantic/ui_renderer.py#L1341
with st.form(key="pydantic_form"):
    input_model = sp.pydantic_input(key="mc_input_model", model=pydModelCard, group_optional_fields="expander")
    submit = st.form_submit_button(label="update")


