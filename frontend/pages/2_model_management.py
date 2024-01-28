import streamlit as st
import model_card_toolkit as mctlib

import streamlit_pydantic as sp

from src.utils import *
from src.schemas import *
from src.backend_test import BACKEND_TEST

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
        submit = st.form_submit_button(label="submit")

    if submit:
        test_backend = BACKEND_TEST()
        ftype = input_model["interface"]["feature_type"]
        endpoint = input_model["interface"]["api_url"]
        if test_backend.check_endpoints(ftype, endpoint):
            st.info("Interface validation passed!")
            #proceed with assessments
            graphics = test_backend.fairness_assess()

            # initialize mdc and toolkit  
            mct = mctlib.ModelCardToolkit()
            #ref https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/core.py#L300
            model_card = mct.scaffold_assets() 

            model_card.quantitative_analysis.graphics.collection = [
                mctlib.Graphic(name='Fairness', image=graphics),
            ]
            #update mdc into toolkit
            mct.update_model_card(model_card)

            # Return the model card document as an HTML page
            html = mct.export_format()

            #debug print
            #print(html)

            # to render HTML string with streamlit: https://docs.streamlit.io/library/components/components-api

            st.components.v1.html(html, height=700, scrolling=True)
        else:
            st.warning("Interface validation failed!")

        #update mct and store proto
          
        
        
        


if st.session_state.user_logged_in:
    show_create_new_assessment()
else:
    st.write("You must log in first to start an assessment job.")
    if st.button("Go to User Management Page"):
        st.switch_page("pages/1_user_management.py")
