import google.generativeai as genai
import streamlit as st
from .schemas import *
from src.utils import *

streamlit_session_states_init()

"""
class pydRAIIA_AIEthicsPrinciplesTemplate(BaseModel):
  whether_or_how_the_solution_addresses_the_factor : str = Field(..., format="multi-line", description="Answer to the question above")
  risk_rating : EnumRAIARiskLevel = Field(..., description="risk rating before mitigation") 
  mitigation_measures : str = Field(..., format="multi-line", description="elaborate your measures to mitigate the risk")
  revised_risk_rating : EnumRAIARiskLevel = Field(..., description="risk rating after mitigation") 
"""


GOOGLE_API_KEY = st.session_state.confs['genai']['api_key']
MODEL_TYPE = st.session_state.confs['genai']['model']

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_TYPE)

SYSTEM_MSG_RISK_ASSESSMENT = """
Analyse the quenstions and answers given by user below on Responsible AI risk assessment. 
Questions will start with 'Q:' and answers with 'A:'.

"""

SUMMARISATION_PROMPT = "Summarise the answers and comment whether the user has done enough due diligence in doing risk assessment."
SUGGESTION_PROMPT = "Suggest to user how his/her orgarnisation can improve."


def generate_response(prompt=""):
    return model.generate_content(prompt)

def compose_qa (model, questions):
    #print(f"input_model: {model}\n")
    qa = ""
    for idx, (att1, val1) in enumerate(model.items()): 
         # risk_factor pydRAIIA_AIEthicsPrinciplesTemplate
         #print(questions[idx], val1)
        qa  += f"Q: {questions[idx]}\n"
        for att2, val2 in val1.items():
            #print(att2, val2)
            if "whether_or_how_the_solution_addresses_the_factor" == att2:
                qa  += f"A: {val2}\n"
            elif "mitigation_measures" == att2: 
                qa  += f"M: {val2}\n\n"
    #print(qa)










