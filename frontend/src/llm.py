import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import streamlit as st
from .schemas import *
from src.utils import *

streamlit_session_states_init()

"""
The finish_reason field in the response from Google Generative AI indicates the reason why the model stopped generating tokens. It can take on the following values:
0 - FINISH_REASON_UNSPECIFIED : The finish reason is unspecified.
1 - STOP : Natural stop point of the model or provided stop sequence.
2 - MAX_TOKENS : The maximum number of tokens as specified in the request was reached.
3 - SAFETY : The token generation was stopped as the response was flagged for safety reasons.
4 - RECITATION : The token generation was stopped as the response was flagged for unauthorized citations.
5 - OTHER : The token generation was stopped due to other reasons.
"""
#ref: https://ai.google.dev/api/python/google/generativeai
#safety settings: https://ai.google.dev/docs/safety_setting_gemini

GOOGLE_API_KEY = st.session_state.confs['genai']['api_key']
MODEL_TYPE = st.session_state.confs['genai']['model']

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_TYPE,
    generation_config = genai.GenerationConfig(
        temperature=0.4,
        top_p = 0.9
    ),
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)


SUMMARISATION_PROMPT = "Summarise the answers and comment whether the user has done enough due diligence in doing risk assessment."
SUGGESTION_PROMPT = "Suggest to user how his/her orgarnisation can improve."


def generate_response(prompt=""):
    response = model.generate_content(prompt)
    try:
        #print(response.text)
        return response.text
    except ValueError:
        # If the response doesn't contain text, check if the prompt was blocked.
        print(response.prompt_feedback)
        # Also check the finish reason to see if the response was blocked.
        print(response.candidates[0].finish_reason)
        # If the finish reason was SAFETY, the safety ratings have more details.
        print(response.candidates[0].safety_ratings)
        return ""
    

def compose_riskassessment_qa (input_model, questions, ai_principle = "Fairness"):
    SYSTEM_MSG_RISK_ASSESSMENT = f"""
        Analyse the risk assessment answers given by an organisation below on questions related to AI ethical principle of {ai_principle}, and mitigation effort taken to minimise or elimintate the risk. 
        Questions will start with 'Q:', answers with 'A:' and mitigation efforts with 'M:'.
        """
    qa = ""
    for idx, (att1, val1) in enumerate(input_model.items()): 
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
                
def ai_assist_risk_assessment_principles (input_model, questions=[], risk_context=[], principle="Fairness and Discrimination"):
    RISK_OPENING = f"You will review the Answer given by user to question on Responsible AI Risk Assessment, particularly on {principle} Risk Factor below, with risk rating in integer from 0 to 5, where 0 = no risk, 5 = Very High Risk."
    MITIGATION_OPENING = f"You will then review the Mitigation solution given. Rate the Revised Risk rating of the risk factor in integer from 0 to 5, where 0 = no risk, 5 = Very High Risk, depending on whether the mitigation method can reduce/eliminate the risk factor."
    COMMON = """If the user doesnt answer the question, or the answer is not relevant, you rate it with risk of 5.
    Constraint: generate your response in JSON with 4 keys, 'Risk:' for risk rating integer before mitigation, 'Reason:' to state your justification for the risk rating, 
    'Revised Risk': for revised risk rating integer when the mitigation step is taken, 'Reason for Revised Risk': the justification for the revised risk rating.
    """
    risk_rating_list = []
    
    for idx, (att1, val1) in enumerate(input_model.items()): 
        qa = RISK_OPENING + MITIGATION_OPENING + risk_context[idx] + COMMON 
        qa  += f"Question: {questions[idx]}\n"
        for att2, val2 in val1.items():
            #print(att2, val2)
            if "whether_or_how_the_solution_addresses_the_factor" == att2:
                qa += f"Answer: {val2}\n"

            if "mitigation_measures" == att2: 
                qa += f"Mitigation: {val2}\n"
                risk_rating = generate_response(qa) 
                risk_rating_list += [risk_rating]
                print("qa: ", qa)
                print("risk rating given:", risk_rating, "\n\n")


    #print(qa)
                


#Based on the answer given to our question, give your risk assessment to the answer in integer from 0 to 5, where 0 = no risk, 1 for Very Low Risk, 2 for Low Risk , 3 for Medium Risk, 4 for High Risk and 5 for Very High Risk. 
#Risk means the potential impact to stake-holders, general public, fundamental and human rights, data privacy, infringement of laws and regulations, etc. 
def ai_assist_risk_assessment_keyfactors(key_factormodel, questions):
    system_prompt = """
    You will review the answer given by user to question on Responsible AI Risk Assessment.
    Estimate the AI ethical risk from the answer, with risk factor in integer from 0 to 5, where 0 = no risk, 5 = Very High Risk.
    If the user doesnt answer the question, or the answer is not relevant, you rate it with risk of 5.
    Constraint: generate your response in JSON with 2 keys, 'Risk:' for risk factor integer, 'Reason:' to state your justification.
    """
    
    for att1, val1 in key_factormodel.items():
        risk_rating_list = []
        for idx1, (att2, val2) in enumerate(val1.items()):
            #print("av2", att2, val2)
            qa = system_prompt + KEYFACTOR_RISK_CONTEXT[idx1]
            qa  += f"\nQuestion: {questions[idx1]}\n"
            #print(questions[idx])
            for att3, val3 in val2.items():
                #print("av3", att3, val3)
                if "answer" == att3:
                    qa  += f"Answer: {val3}\n"
                    #qa  += "Risk:"
                    print("qa: ", qa)
                    risk_rating = generate_response(qa) 
                    print("risk rating given:", risk_rating, "\n\n")
                    risk_rating_list += [risk_rating]
    
    return  risk_rating_list














