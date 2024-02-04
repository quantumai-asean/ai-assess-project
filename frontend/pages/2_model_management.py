import streamlit as st
import model_card_toolkit as mctlib

import streamlit_pydantic as sp
import pandas as pd
from src.utils import *
from src.schemas import *
from src.backend_test import BACKEND_TEST

streamlit_session_states_init()

#experiments on rendering INput Output
st.set_page_config(
    #page_title="Create New Assessment Job",
    page_icon="🚀",
)

def expand_performance_metrics(performance):
    expand_perf = [] #mctlib.PerformanceMetric()
    #{'type': 'accuracy', 'value': cat_accuracy, 'slice': 'cat'},
    if isinstance(performance, pd.DataFrame):
        for c in performance.columns:
            for i in performance.index:
                #element = {'type': c, 'value': performance[c][i], 'slice': i  }
                element = mctlib.PerformanceMetric(type = c, value= "%0.4f" % performance[c][i], slice=i)
                expand_perf.append(element)
    return expand_perf

def set_mcstate(sm:str='', rerun=True):
    st.session_state.modelcardpage_states['sm_showassessment'] = False
    st.session_state.modelcardpage_states['sm_showmodelcard'] = False
    st.session_state.modelcardpage_states['sm_RunAssessment'] = False
    if sm:
        st.session_state.modelcardpage_states[sm] = True
    if rerun:
        st.rerun()


def show_create_new_assessment():
    st.title("Create New Assessment Job")

    #or idea: https://github.com/LukasMasuch/streamlit-pydantic/blob/390a45aba7bf8caccc297c335715cc141db490af/src/streamlit_pydantic/ui_renderer.py#L1341
    with st.form(key="model_registration_form"):
        input_model = sp.pydantic_input(key="mc_input_model", model=pydModelCard, group_optional_fields="expander")
        submit = st.form_submit_button(label="Start Assessment")
        st.session_state.modelcardpage_states['sm_RunAssessment'] = False
        if submit:
            st.session_state.modelcardpage_states['mc_registration_input'] = input_model
            st.session_state.modelcardpage_states['sm_showassessment'] = True
            st.session_state.modelcardpage_states['sm_showmodelcard'] = False
            st.session_state.modelcardpage_states['sm_RunAssessment'] = True
            #set_mcstate('sm_showassessment')
            st.rerun()





          
def show_modelassessment():
    st.title("Model Assessment")
    if st.session_state.modelcardpage_states['sm_RunAssessment']:
        
        test_backend = BACKEND_TEST()
        input_model = st.session_state.modelcardpage_states['mc_registration_input']
        ftype = input_model["interface"]["feature_type"]
        endpoint = input_model["interface"]["api_url"]
        if test_backend.check_endpoints(ftype, endpoint):
            st.info("Interface validation passed! Running Asssessment.")
            # initialize mdc and toolkit  
            mct = mctlib.ModelCardToolkit()
            #ref https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/core.py#L300
            model_card = mct.scaffold_assets() 
            model_card.model_details.name = input_model["model_details"]["name"]
            model_card.model_details.overview = input_model["model_details"]["overview"]
            model_card.model_details.owners = [
                mctlib.Owner(name=st.session_state.user_details['name'], contact=st.session_state.user_details['email'])
            ]
            model_card.model_details.version.name = input_model["versioning"]["version_name"]

            #proceed with assessments
            #https://www.tensorflow.org/responsible_ai/model_card_toolkit/api_docs/python/model_card_toolkit/QuantitativeAnalysis
            performance, graphics = test_backend.fairness_assess() # shd be the entire qualitative assessment

            model_card.quantitative_analysis.performance_metrics = expand_performance_metrics(performance)

            model_card.quantitative_analysis.graphics.collection = [
                mctlib.Graphic(name='Fairness Metrics', image=graphics),
            ]

            mct.update_model_card(model_card)

            st.session_state.modelcardpage_states['mc_modelcard'] = model_card
            st.session_state.modelcardpage_states['mc_mctoolkit'] = mct

            st.session_state.modelcardpage_states['sm_RunAssessment'] = False
            st.rerun()
        else:
            st.warning("Interface validation failed!")
            if st.button("Return to Model Card Form"):
                set_mcstate()

    else:
        set_mcstate('sm_showmodelcard')

def show_modelcard():
    st.title("Model Assessment Card")
    st.info("Model Assessment Completed")
    with st.form(key="show_modelcard_form"):
        
        mct = st.session_state.modelcardpage_states['mc_mctoolkit'] 
        model_card = st.session_state.modelcardpage_states['mc_modelcard']
        # Return the model card document as an HTML page
        #update mdc into toolkits
        html = mct.export_format()
        st.components.v1.html(html, height=1200, scrolling=True)
        submit = st.form_submit_button(label="Save Model Card")

        if submit:
            st.info("Saving Model Card")
            mc_json = model_card.to_json()
            query_str = f"""INSERT INTO modelcard (name, version, email, modelcard_data) 
            VALUES ('{model_card.model_details.name}','{model_card.model_details.version.name}','{st.session_state.user_details['email']}','{mc_json}'::jsonb);"""
            if psql_database_interface(qry=query_str, configs = st.session_state.confs['database']['server'], action="update"):
                st.info("Model Card saved succesfully!")

    if st.button("run another assessment"):
        set_mcstate()

        
        


if st.session_state.user_logged_in:
    if st.session_state.modelcardpage_states['sm_showmodelcard']:
        show_modelcard()
    elif st.session_state.modelcardpage_states['sm_showassessment']:
        show_modelassessment()
    else:
        show_create_new_assessment()
    
else:
    st.write("You must log in first to start an assessment job.")
    if st.button("Go to User Management Page"):
        st.switch_page("pages/1_user_management.py")
