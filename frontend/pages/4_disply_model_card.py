import model_card_toolkit as mctlib
import streamlit as st
from datetime import date
import uuid
import os
from src.schemas import *
from src.llm import ai_assist_risk_assessment_principles, ai_assist_risk_assessment_keyfactors
from src.enums import  RISK_LEVEL 


# tutorial from https://www.tensorflow.org/responsible_ai/model_card_toolkit/examples/Scikit_Learn_Model_Card_Toolkit_Demo

def compose_saKeyFactorUserAnswer (key_factormodel):
  answers = []
  for att1, val1 in key_factormodel.items():
    for att2, val2 in val1.items():
      answers.append(val2)
  return answers



def display_self_assessment_mc():
    # initialize mdc and toolkit
    mct_directory = "."
    mct = mctlib.ModelCardToolkit(mct_directory)

    model_card = mct.scaffold_assets()

    ## annotate information
    #model_card.model_details.name = 'Breast Cancer Wisconsin (Diagnostic) Dataset'
    #model_card.model_details.overview = (
    #    'This model predicts whether breast cancer is benign or malignant based on '
    #    'image measurements.')
    #model_card.model_details.owners = [
    #    mctlib.Owner(name= 'Model Cards Team', contact='model-cards@google.com')
    #]
    #model_card.model_details.references = [
    #    mctlib.Reference(reference='https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)'),
    #    mctlib.Reference(reference='https://minds.wisconsin.edu/bitstream/handle/1793/59692/TR1131.pdf')
    #]
    #model_card.model_details.version.name = str(uuid.uuid4())
    #model_card.model_details.version.date = str(date.today())

    #model_card.considerations.ethical_considerations = [mctlib.Risk(
    #    name=('Manual selection of image sections to digitize could create '
    #            'selection bias'),
    #    mitigation_strategy='Automate the selection process'
    #)]
    #model_card.considerations.limitations = [mctlib.Limitation(description='Breast cancer diagnosis')]
    #model_card.considerations.use_cases = [mctlib.UseCase(description='Breast cancer diagnosis')]
    #model_card.considerations.users = [mctlib.User(description='Medical professionals'), mctlib.User(description='ML researchers')]


    #test custom model
    # Project Summary

    if 'manual_assessment_projectsummary' in st.session_state:
        model_card.saProjectSummary.background.project_name = st.session_state.manual_assessment_projectsummary ['background']['project_name']
        model_card.saProjectSummary.background.business_segment = st.session_state.manual_assessment_projectsummary ['background']['business_segment']
        model_card.saProjectSummary.background.project_start_date = st.session_state.manual_assessment_projectsummary ['background']['project_start_date'].strftime("%d-%m-%Y")
        model_card.saProjectSummary.background.ai_system_launch_date = st.session_state.manual_assessment_projectsummary ['background']['ai_system_launch_date'].strftime("%d-%m-%Y")
        model_card.saProjectSummary.background.region = st.session_state.manual_assessment_projectsummary ['background']['region']
        model_card.saProjectSummary.background.responsible_person = st.session_state.manual_assessment_projectsummary ['background']['responsible_person']

        model_card.saProjectSummary.summary.high_level_technical_and_functional_overview = st.session_state.manual_assessment_projectsummary ['summary']['high_level_technical_and_functional_overview']
        model_card.saProjectSummary.summary.business_driver_and_context = st.session_state.manual_assessment_projectsummary ['summary']['business_driver_and_context']
        model_card.saProjectSummary.summary.external_data_sources_and_data_sets = st.session_state.manual_assessment_projectsummary ['summary']['external_data_sources_and_data_sets']
        model_card.saProjectSummary.summary.internal_data_sources_and_data_sets = st.session_state.manual_assessment_projectsummary ['summary']['internal_data_sources_and_data_sets']
        model_card.saProjectSummary.summary.legal_risk = st.session_state.manual_assessment_projectsummary ['summary']['summary_of_potential_risks']['legal_risk']
        model_card.saProjectSummary.summary.reputational_risk = st.session_state.manual_assessment_projectsummary ['summary']['summary_of_potential_risks']['reputational_risk']
        model_card.saProjectSummary.summary.ethical_risk = st.session_state.manual_assessment_projectsummary ['summary']['summary_of_potential_risks']['ethical_risk']
        model_card.saProjectSummary.summary.environmental_risk = st.session_state.manual_assessment_projectsummary ['summary']['summary_of_potential_risks']['environmental_risk']
        model_card.saProjectSummary.summary.external_related_documents = st.session_state.manual_assessment_projectsummary ['summary']['external_related_documents']
        model_card.saProjectSummary.summary.governance_model = st.session_state.manual_assessment_projectsummary ['summary']['governance_model']
        model_card.saProjectSummary.summary.project_team = st.session_state.manual_assessment_projectsummary ['summary']['project_team']

    if 'manual_assessment_keyfactor' in st.session_state:
        #print("keyfactor user submission:",st.session_state.manual_assessment_keyfactor)
        user_answers = compose_saKeyFactorUserAnswer(st.session_state.manual_assessment_keyfactor)
        #print("composed user answers:", user_answers)
        #print(model_card.saKeyFactors.keyfactor)
        #print("Keyfactor AI rated risk[0]: ", st.session_state.manual_assessment_keyfactor_ai_review[0], type(st.session_state.manual_assessment_keyfactor_ai_review[0]))
        #model_card.saKeyFactors.keyfactor = [ mctlib.saKeyFactorField(risk_factor_question=KEYFACTOR_QUESTIONS[0], 
        #                                                              risk_factor_answer=user_answers[0]['answer'],
        #                                                              user_risk_rating=RISK_LEVEL[user_answers[0]['predicted_risk']],
        #                                                              ai_risk_rating=RISK_LEVEL[st.session_state.manual_assessment_keyfactor_ai_review[0]['Risk']],
        #                                                              ai_risk_reason=st.session_state.manual_assessment_keyfactor_ai_review[0]['Reason']
        #                                                               ) ]
        for kf_q, usr_a, ai_rv in zip(KEYFACTOR_QUESTIONS, user_answers, st.session_state.manual_assessment_keyfactor_ai_review):
            model_card.saKeyFactors.keyfactor += [ mctlib.saKeyFactorField(risk_factor_question=kf_q, 
                                                                      risk_factor_answer=usr_a['answer'],
                                                                      user_risk_rating=RISK_LEVEL[usr_a['predicted_risk']],
                                                                      ai_risk_rating=RISK_LEVEL[ai_rv['Risk']],
                                                                      ai_risk_reason=ai_rv['Reason']
                                                                       ) ]
        #print(model_card.saKeyFactors.keyfactor)



        
        #print(model_card.saKeyFactors.keyfactor)




    #update mdc into toolkit
    mct.update_model_card(model_card)


    template_path = os.path.join(mct_directory, "template/html/sat_rai_mc.html.jinja")

    # Return the model card document as an HTML page
    #html = mct.export_format()

    #html = mct.export_format(model_card, template_path, "test_mc.html")
    #need to pass addtional fields to export_format call ... they can exist externally
    template_variables = {
        'saProjectSummary': model_card.saProjectSummary,
        'saKeyFactors': model_card.saKeyFactors,
        'saRAIIARiskAssessment' : model_card.saRAIIARiskAssessment
        }
    html = mct.export_format(model_card, template_path, template_variables = template_variables)

    #debug print
    #print(html)

    # to render HTML string with streamlit: https://docs.streamlit.io/library/components/components-api

    st.components.v1.html(html, height=700, scrolling=True)





if 'updating_selfassess_mc' not in st.session_state:
    st.session_state['updating_selfassess_mc'] = False

if st.session_state['updating_selfassess_mc'] == False:
    if st.button("Submit Self-Assessment"):
        st.session_state['updating_selfassess_mc'] = True
        st.rerun()
else:
    with st.spinner('Engaging AI Review, please wait and do not refresh the page'):
        if 'manual_assessment_keyfactor' in st.session_state:
            keyfactor_model = st.session_state.manual_assessment_keyfactor
            #st.session_state.manual_assessment_keyfactor_user_total_risk = calculate_risk_points(input_model)
            st.session_state.manual_assessment_keyfactor_ai_review = ai_assist_risk_assessment_keyfactors(keyfactor_model, KEYFACTOR_QUESTIONS) #to be processed later 
            print("Keyfactor AI rated risk: ", st.session_state.manual_assessment_keyfactor_ai_review)

    display_self_assessment_mc()
    st.session_state['updating_selfassess_mc'] = False
    if st.button("Rerun"):
        st.session_state['updating_selfassess_mc'] = True
        st.rerun()





