import model_card_toolkit as mctlib
import streamlit as st
from datetime import date
import uuid

# tutorial from https://www.tensorflow.org/responsible_ai/model_card_toolkit/examples/Scikit_Learn_Model_Card_Toolkit_Demo


# initialize mdc and toolkit
mct = mctlib.ModelCardToolkit()

model_card = mct.scaffold_assets()

# annotate information
model_card.model_details.name = 'Breast Cancer Wisconsin (Diagnostic) Dataset'
model_card.model_details.overview = (
    'This model predicts whether breast cancer is benign or malignant based on '
    'image measurements.')
model_card.model_details.owners = [
    mctlib.Owner(name= 'Model Cards Team', contact='model-cards@google.com')
]
model_card.model_details.references = [
    mctlib.Reference(reference='https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)'),
    mctlib.Reference(reference='https://minds.wisconsin.edu/bitstream/handle/1793/59692/TR1131.pdf')
]
model_card.model_details.version.name = str(uuid.uuid4())
model_card.model_details.version.date = str(date.today())

model_card.considerations.ethical_considerations = [mctlib.Risk(
    name=('Manual selection of image sections to digitize could create '
            'selection bias'),
    mitigation_strategy='Automate the selection process'
)]
model_card.considerations.limitations = [mctlib.Limitation(description='Breast cancer diagnosis')]
model_card.considerations.use_cases = [mctlib.UseCase(description='Breast cancer diagnosis')]
model_card.considerations.users = [mctlib.User(description='Medical professionals'), mctlib.User(description='ML researchers')]

#update mdc into toolkit
mct.update_model_card(model_card)

# Return the model card document as an HTML page
html = mct.export_format()

#debug print
#print(html)

# to render HTML string with streamlit: https://docs.streamlit.io/library/components/components-api

st.components.v1.html(html, height=700, scrolling=True)