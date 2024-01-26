import streamlit as st
import model_card_toolkit as mctlib
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

from src.utils import *
from src.schemas import *

streamlit_session_states_init()

#experiments on rendering INput Output
st.set_page_config(
    page_title="Create New Assessment Job",
    page_icon="🚀",
)

def show_create_new_assessment():
    st.title("Create New Assessment Job")

    #or idea: https://github.com/LukasMasuch/streamlit-pydantic/blob/390a45aba7bf8caccc297c335715cc141db490af/src/streamlit_pydantic/ui_renderer.py#L1341
    with st.form(key="pydantic_form"):
        input_model = sp.pydantic_input(key="mc_input_model", model=pydModelCard, group_optional_fields="expander")
        submit = st.form_submit_button(label="update")

    if submit:
        #update mct and store proto
        # initialize mdc and toolkit
        mct = mctlib.ModelCardToolkit()

        model_card = mct.scaffold_assets() #ref https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/core.py#L300

        # ....

if st.session_state.user_logged_in:
    show_create_new_assessment()
else:
    st.write("You must log in first to start an assessment job.")
    if st.button("Go to User Management Page"):
        st.switch_page("pages/1_user_management.py")
