import streamlit as st
import model_card_toolkit as mctlib

import streamlit_pydantic as sp
import pandas as pd
from src.utils import *
from src.schemas import *
from src.backend_test import BACKEND_TEST

from src.llm import ai_assist_risk_assessment_principles, ai_assist_risk_assessment_keyfactors

streamlit_session_states_init()

#experiments on rendering INput Output
st.set_page_config(
    #page_title="Create New Assessment Job",
    page_icon="🚀",
)

TOTAL_PRE_SURVEY_PAGECNT = 10

def next_page():
    if st.session_state.modelcardpage_states['sm_registration_page_cnt'] + 1 <= TOTAL_PRE_SURVEY_PAGECNT:
        st.session_state.modelcardpage_states['sm_registration_page_cnt'] += 1
    st.rerun()
    
    
    

def previous_page():
    if st.session_state.modelcardpage_states['sm_registration_page_cnt'] > 0:
        st.session_state.modelcardpage_states['sm_registration_page_cnt'] -= 1


def show_prev_next_buttons():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏮️ Back", on_click=previous_page):
            pass

#    with col2:
#        if st.button("Next ⏭️", on_click=next_page):
#            pass

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
    show_prev_next_buttons()
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
    scroll_to_top(st.session_state.modelcardpage_states['sm_registration_page_cnt'])


          
def show_modelassessment():
    st.title("Model Assessment")
    #print("Hi!")
    if st.session_state.modelcardpage_states['sm_RunAssessment']:
        #print("hello")
        test_backend = BACKEND_TEST()
        input_model = st.session_state.modelcardpage_states['mc_registration_input']
        ftype = input_model["interface"]["feature_type"]
        endpoint = input_model["interface"]["api_url"]
        if test_backend.check_endpoints(ftype, endpoint):
            #print("ok")
            st.info("Interface validation passed!")
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
            with st.spinner('Running Asssessments...'):
                performance, graphics = test_backend.fairness_assess() # shd be the entire qualitative assessment

            model_card.quantitative_analysis.performance_metrics = expand_performance_metrics(performance)

            model_card.quantitative_analysis.graphics.collection = [
                mctlib.Graphic(name='Fairness Metrics', image=graphics),
            ]

            mct.update_model_card(model_card)

            st.session_state.modelcardpage_states['mc_modelcard'] = model_card
            st.session_state.modelcardpage_states['mc_mctoolkit'] = mct

            st.session_state.modelcardpage_states['sm_RunAssessment'] = False
            st.session_state.modelcardpage_states['mc_saved'] = False
            st.rerun()
        else:
            st.warning("Interface validation failed!")
            if st.button("Return to Model Card Form"):
                set_mcstate()

    else:
        set_mcstate('sm_showmodelcard')

def show_modelcard():
    st.title("Model Assessment Card")
    #st.info("Model Assessment Completed")

    mct = st.session_state.modelcardpage_states['mc_mctoolkit'] 
    model_card = st.session_state.modelcardpage_states['mc_modelcard']
    # Return the model card document as an HTML page
    #update mdc into toolkits
    html = mct.export_format()
    st.components.v1.html(html, height=1200, scrolling=True)

    if not st.session_state.modelcardpage_states['mc_saved']:
        if st.button("save model card"):
            st.info("Saving Model Card")
            mc_json = model_card.to_json()
            query_str = f"""INSERT INTO modelcard (name, version, email, modelcard_data) 
            VALUES ('{model_card.model_details.name}','{model_card.model_details.version.name}','{st.session_state.user_details['email']}','{mc_json}'::jsonb);"""
            if psql_database_interface(qry=query_str, configs = st.session_state.confs['database']['server'], action="update"):
                st.info("Model Card saved succesfully!")
            st.session_state.modelcardpage_states['mc_saved'] = True
            st.rerun()
    if st.session_state.user_logged_in:
        if st.button("run another assessment"):
            set_mcstate()
    else:
        if st.button("Go to User Management Page"):
            st.switch_page("pages/1_user_management.py")


#PreAssessment 


        


def assessment_landing_page():
    st.title("Model Assessment")
    with st.form(key="preAss_page0"):
        input_model = sp.pydantic_input(key="mc_preAss_page1", model=pydAssessmentLandingPage, group_optional_fields="expander")
        submit = st.form_submit_button(label="Confirm")
        if submit:
            if EnumRAIAPage1Choice(input_model['select_assessment_mode']).name == EnumRAIAPage1Choice.LOAD:
                #load show load page
                pass
            else:
                #show select new assessment
                # check if it involves model assessment? questionaires are compulsory ...
                # Use RAIIA adapted template
                # pass
                st.session_state.modelcardpage_states['sm_registration_page_cnt'] = 2
                st.rerun()

            #next_page()

def print_model_propteries(model):
    #str_properties = {attr: value for attr, value in model.items() if 'risk_rating'==attr}
    #print('check prop:', str_properties)
    for attr1, value1 in model.items():
        for attr2, value2 in value1.items():
            if "risk_rating" in attr2:
                print('check prop:', value2)

def calculate_risk_points(model):
    #str_properties = {attr: value for attr, value in model.items() if 'risk_rating'==attr}
    #print('check prop:', str_properties)

    total_risks = {'risk_rating':0, 'revised_risk_rating':0}

    for _, value1 in model.items():
        for attr2, value2 in value1.items():
            if attr2 == 'risk_rating':
                total_risks["risk_rating"]  += value2
            elif attr2 == 'revised_risk_rating':
                total_risks["revised_risk_rating"] += value2

    return total_risks



def manual_assessment_projectsummary():
    st.title("Project Summary")
    with st.form(key="preAss_projectsummary"):
        if 'manual_assessment_projectsummary' in st.session_state:
            model = pydRAIIA_ProjectSummary.model_validate(st.session_state.manual_assessment_projectsummary)
        else:
            model = pydRAIIA_ProjectSummary

        input_model = sp.pydantic_input(key="mc_preAss_projectsummary", model=model, group_optional_fields="expander")
        
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_projectsummary = input_model
            next_page()


def manual_assessment_keyfactor():
    st.title("Identifying Key Factors")
    with st.form(key="preAss_keyfactor"):
        if 'manual_assessment_keyfactor' in st.session_state:
            model = pydRAIIA_Keyfactor.model_validate(st.session_state.manual_assessment_keyfactor)
        else:
            model = pydRAIIA_Keyfactor
        input_model = sp.pydantic_input(key="mc_preAss_keyfactor", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_keyfactor = input_model
            #st.session_state.manual_assessment_keyfactor_user_total_risk = calculate_risk_points(input_model)
            #st.session_state.manual_assessment_keyfactor_ai_rated_risk = ai_assist_risk_assessment_keyfactors(input_model, KEYFACTOR_QUESTIONS) #to be processed later 
            next_page()

def check_props (input_class):
    schema_properties = input_class.schema(by_alias=True).get(
            "properties", {}
        )
    required_properties = input_class.schema(by_alias=True).get(
            "required", []
        )
    print(schema_properties)
    

def manual_assessment_fairness():
    st.title("Principle: Fairness")
    with st.form(key="preAss_fairness"):
        if 'manual_assessment_fairness' in st.session_state:
            model = pydRAIIA_FairnessAssessment.model_validate(st.session_state.manual_assessment_fairness) # doesnt show enum
        else:
            model = pydRAIIA_FairnessAssessment 
        input_model = sp.pydantic_input(key="mc_preAss_fairness", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:          
            #save to table tied to user 1
            st.session_state.manual_assessment_fairness = input_model
            st.session_state.manual_assessment_fairness_total_risk = calculate_risk_points(input_model)
            #compose_riskassessment_qa(input_model, FAIR_QUESTIONS)
            #ai_assist_risk_assessment_principles(input_model, FAIR_QUESTIONS, FAIR_RISK_CONTEXT, "Fairness and Discrimination")
            next_page()

def manual_assessment_reliability():
    st.title("Principle: Reliability, Safety and Control")
    with st.form(key="preAss_reliability"):
        if 'manual_assessment_reliability' in st.session_state:
            model = pydRAIIA_ReliabilityAssessment.model_validate(st.session_state.manual_assessment_reliability)
        else:
            model = pydRAIIA_ReliabilityAssessment
        input_model = sp.pydantic_input(key="mc_preAss_reliability", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_reliability = input_model
            st.session_state.manual_assessment_reliability_total_risk = calculate_risk_points(input_model)
            next_page()


def manual_assessment_privacysecurity():
    st.title("Principle: Privacy and Security")
    with st.form(key="preAss_privacysecurity"):
        if 'manual_assessment_privacysecurity' in st.session_state:
            model = pydRAIIA_PrivacyAssessment.model_validate(st.session_state.manual_assessment_privacysecurity)
        else:
            model = pydRAIIA_PrivacyAssessment
        input_model = sp.pydantic_input(key="mc_preAss_privacysecurity", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_privacysecurity = input_model
            st.session_state.manual_assessment_privacysecurity_total_risk = calculate_risk_points(input_model) 
            next_page()


def manual_assessment_accountability():
    st.title("Principle: Accountability")
    with st.form(key="preAss_accountability"):
        if 'manual_assessment_accountability' in st.session_state:
            model = pydRAIIA_AccountabilityAssessment.model_validate(st.session_state.manual_assessment_accountability)
        else:
            model = pydRAIIA_AccountabilityAssessment
        input_model = sp.pydantic_input(key="mc_preAss_accountability", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_accountability = input_model
            st.session_state.manual_assessment_accountability_total_risk = calculate_risk_points(input_model)
            next_page()


def manual_assessment_transparency():
    st.title("Principle: Transparency")
    with st.form(key="preAss_transparency"):
        if 'manual_assessment_transparency' in st.session_state:
            model = pydRAIIA_TransparencyAssessment.model_validate(st.session_state.manual_assessment_transparency)
        else:
            model = pydRAIIA_TransparencyAssessment
        input_model = sp.pydantic_input(key="mc_preAss_transparency", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_transparency = input_model
            st.session_state.manual_assessment_transparency_total_risk = calculate_risk_points(input_model)
            next_page()


def manual_assessment_humanhappiness():
    st.title("Principle: Pursuit of human benefits and happiness")
    with st.form(key="preAss_humanhappiness"):
        if 'manual_assessment_humanhappiness' in st.session_state:
            model = pydRAIIA_HumanHappinessAssessment.model_validate(st.session_state.manual_assessment_humanhappiness)
        else:
            model = pydRAIIA_HumanHappinessAssessment
        input_model = sp.pydantic_input(key="mc_preAss_humanhappiness", model=model, group_optional_fields="expander")
        submit = st.form_submit_button(label="submit")
        if submit:
            #save to table tied to user 1
            st.session_state.manual_assessment_humanhappiness = input_model
            st.session_state.manual_assessment_humanhappiness_total_risk = calculate_risk_points(input_model)
            next_page()
            

def load_algoassessment_record():
    show_prev_next_buttons()
    st.write("load algo assessment record")
    st.write("under construction")

preassessment_survey_pages = {
    0: assessment_landing_page,
    1: load_algoassessment_record, # load pre-registered model assessment
    2: manual_assessment_projectsummary, # start RAIIA questionaires -> project summary
    3: manual_assessment_keyfactor, # start RAIIA questionaires -> key factor
    4: manual_assessment_fairness, 
    5: manual_assessment_reliability,
    6: manual_assessment_privacysecurity,
    7: manual_assessment_accountability,
    8: manual_assessment_transparency,
    9: manual_assessment_humanhappiness,
    #TOTAL_PRE_SURVEY_PAGECNT: assessment_landing_page
}



def show_preassessment_survey():
#    col1, col2 = st.columns(2)
    show_prev_next_buttons()
    idx = st.session_state.modelcardpage_states['sm_registration_page_cnt']
    preassessment_survey_pages[idx]()
    scroll_to_top(st.session_state.modelcardpage_states['sm_registration_page_cnt'])
    
    
#    with col1:
#        if st.button("⏮️ Back", on_click=previous_page):
#            pass

#    with col2:
#        if st.button("Next ⏭️", on_click=next_page):
#            pass




#state machine
if st.session_state.user_logged_in:
    if st.session_state.modelcardpage_states['sm_showmodelcard']:
        show_modelcard()
    elif st.session_state.modelcardpage_states['sm_showassessment']:
        show_modelassessment()
    else:
        st.session_state.modelcardpage_states['mc_saved'] = False
        st.write(st.session_state.modelcardpage_states['sm_registration_page_cnt'])
        # start with page 1
        if st.session_state.modelcardpage_states['sm_registration_page_cnt'] < TOTAL_PRE_SURVEY_PAGECNT:
            show_preassessment_survey()
        else:   
            show_create_new_assessment()
elif len(st.query_params.get_all("mc"))>0:
    mc_id = int(st.query_params.get_all("mc")[0])
    st.session_state.modelcardpage_states['mc_saved'] = True

    configs = st.session_state.confs['database']['server']
    qry_str = f"SELECT modelcard_data FROM modelcard WHERE id = {mc_id};"
    action_str = "query"
    r = psql_database_interface(qry_str, configs, action_str)
    mc_json = r[0][0]
    st.session_state.modelcardpage_states['mc_mctoolkit']= mct = mctlib.ModelCardToolkit()
    st.session_state.modelcardpage_states['mc_modelcard'] = mct.scaffold_assets(mc_json)
    show_modelcard()

else:
    st.write("You must log in first to start an assessment job.")
    if st.button("Go to User Management Page"):
        st.switch_page("pages/1_user_management.py")


