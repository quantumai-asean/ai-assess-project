import model_card_toolkit as mctlib
import streamlit as st
from datetime import date
import uuid
import os

# tutorial from https://www.tensorflow.org/responsible_ai/model_card_toolkit/examples/Scikit_Learn_Model_Card_Toolkit_Demo


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
    print(st.session_state.manual_assessment_keyfactor)



#update mdc into toolkit
mct.update_model_card(model_card)


template_path = os.path.join(mct_directory, "template/html/sat_rai_mc.html.jinja")

# Return the model card document as an HTML page
#html = mct.export_format()

#html = mct.export_format(model_card, template_path, "test_mc.html")
#need to pass addtional fields to export_format call ... they can exist externally
template_variables = {
    'saProjectSummary': model_card.saProjectSummary,
    #keyfactor
    #'saRAIIARiskAssessment' = model_card.saRAIIARiskAssessment
    }
html = mct.export_format(model_card, template_path, template_variables = template_variables)

#debug print
#print(html)

# to render HTML string with streamlit: https://docs.streamlit.io/library/components/components-api

st.components.v1.html(html, height=700, scrolling=True)