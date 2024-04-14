from pydantic import BaseModel, Field, StringConstraints, ConfigDict
import datetime
from typing_extensions import Annotated
import dataclasses
from typing import Any, Dict, List, Optional, Union, Set
from .enums import *

FIRESTORE_USER_COLLECTION = "qai_rai_user_records"
FIRESTORE_ALGO_ASSESSMENT_MC_COLLECTION = "qai_rai_algo_mc_records"
FIRESTORE_SELFMANUAL_ASSESSMENT_MC_COLLECTION = "qai_rai_selfmanual_mc_records"

class pydUserRegistrationInput(BaseModel):
  """The information about owners of a model.

  Attributes:
    name: The name of the model owner.
    email: email
    url: company URL
    country: Dict or List 
    password: hash
  """
  name: Annotated[str, StringConstraints(max_length=50)] = Field(..., description="The company name of the model owner.")
  email: Annotated[str, StringConstraints(max_length=50)] = Field(..., description="Owner's email. Will be used as login prompt. Must not be blank")
  url: Annotated[str, StringConstraints(max_length=50)] = Field(..., description="Owner's company URL.")
  country: EnumCountry = Field(..., description="Select your country from the dropdownlist")
  create_password: Annotated[str, StringConstraints(max_length=30)] = Field(..., writeOnly=True)
  confirm_password: Annotated[str, StringConstraints(max_length=30)] = Field(..., writeOnly=True)

class pydUserLogin(BaseModel):
   email: Annotated[str, StringConstraints(max_length=50)]
   password: Annotated[str, StringConstraints(max_length=30)] = Field(..., writeOnly=True)





# First need to create a pydantic model equivalent of ModelDetails 
# tip : Annotated is a type hint that allows you to attach additional metadata to a type.
class pydModelDetails(BaseModel):
    """https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/model_card.py#L131
    """
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[str, StringConstraints(max_length=30)] = Field(..., description="The name of the model.")
    overview: str = Field(..., format="multi-line", description="A description of the model card. of this")
    #documentation: str = Field(..., description="A more thorough description of the model and its usage.")

class pydOwner(BaseModel):
  """The information about owners of a model.

  Attributes:
    name: The name of the model owner.
    contact: The contact information for the model owner or owners. These could
      be individual email addresses, a team mailing list expressly, or a
      monitored feedback form.
  """
  name: Annotated[str, StringConstraints(max_length=50)] = Field(..., description="The name of the model owner.")
  contact: Annotated[str, StringConstraints(max_length=50)] = Field(..., description="The contact information for the model owner or owners. These could be individual email addresses, a team mailing list expressly, or a monitored feedback form.")

class pydVersion(BaseModel):
  """The information about verions of a model.

  If there are multiple versions of the model, or there may be in the future,
  it’s useful for your audience to know which version of the model is
  discussed
  in the Model Card. If there are previous versions of this model, briefly
  describe how this version is different. If no more than one version of the
  model will be released, this field may be omitted.

  Attributes:
    name: The name of the version.
    date: The date this version was released.
    diff: The changes from the previous version.
  """
  version_name: Annotated[str, StringConstraints(max_length=30)] = Field(..., description="The name of the version.")
  release_date: str = Field(..., description="The date this version was released.")
  changes: str = Field(..., description="The changes from the previous version.")

class pydLicense(BaseModel):
  """The license information for a model.

  Attributes:
    identifier: A standard SPDX license identifier (https://spdx.org/licenses/),
      or "proprietary" for an unlicensed Module.
    custom_text: The text of a custom license.
  """
  identifier: str = Field(..., description="A standard SPDX license identifier (https://spdx.org/licenses/), or \"proprietary\" for an unlicensed Module.")
  custom_text: str = Field(..., description="The text of a custom license.")

class pydReference(BaseModel):
  """Reference for a model.

  Attributes:
    reference: A reference to a resource.
  """
  reference: str = Field(..., description="A reference to a resource.")


class pydCitation(BaseModel):
  """A citation for a model.

  Attributes:
    style: The citation style, such as MLA, APA, Chicago, or IEEE.
    citation: the citation.
  """
  style: str = Field(..., description="The citation style, such as MLA, APA, Chicago, or IEEE.")
  citation: str = Field(..., description="the citation.")

class pydModelDataInterface(BaseModel):
   """How to interface with the model
   Attributes:
      model_api: API endpoint for calling inference function of the model, need validation method
      data_api: API endpoint for sampling for evaluation dataset, must adhere to our format (pytorch), need validation method

   """
   api_url: str = Field(..., description="API URL for calling inference and data sampling functions of the model.")
   #data_api : str  = Field(..., description="API endpoint for sampling evaluation dataset, must adhere to specified format")
   feature_type: EnumFeatureType = Field(..., description="Select the type of feature to the model.")
   model_type: EnumAITaskTypes = Field(..., description="Select the type of the model.") 
   applicable_ethical_assessments: Set[EnumAssessmentTypes]  = Field(..., description="Select the applicable assessments to the model.")



class pydFairnessConsiderations(BaseModel):
  types_of_harms: Set[EnumFairHarmTypes] = Field(..., description="What type of Harm can be associated from the usage of the model?") 

class pydConsiderations(BaseModel):
  """Considerations related to model construction, training, and application.

  The considerations section includes qualitative information about your model,
  including some analysis of its risks and limitations. As such, this section
  usually requires careful consideration, and conversations with many relevant
  stakeholders, including other model developers, dataset producers, and
  downstream users likely to interact with your model, or be affected by its
  outputs.

  Attributes:
    users: Who are the intended users of the model? This may include
      researchers, developers, and/or clients. You might also include
      information about the downstream users you expect to interact with your
      model.
    use_cases: What are the intended use cases of the model? What use cases are
      out-of-scope?
    limitations: What are the known limitations of the model? This may include
      technical limitations, or conditions that may degrade model performance.
    tradeoffs: What are the known accuracy/performance tradeoffs for the model?
    ethical_considerations: What are the ethical risks involved in application
      of this model? For each risk, you may also provide a mitigation strategy
      that you've implemented, or one that you suggest to users.
  """
  target_users: str = Field(..., format="multi-line", description="Who are the intended users of the model? You might also include information about the downstream users you expect to interact with your model.") 
  use_cases: str = Field(..., format="multi-line", description="What are the intended use cases of the model?") 
  #limitations: str = Field(..., format="multi-line", description="What are the known limitations of the model? This may include technical limitations, or conditions that may degrade model performance.") 
  #tradeoffs: str = Field(..., format="multi-line", description=" What are the known accuracy/performance tradeoffs for the model?") 
  ethical_considerations: str = Field(..., format="multi-line", description="What are the ethical risks involved in application of this model? For each risk, you may also provide a mitigation strategy that you've implemented, or one that you suggest to users.") 
  fairness_harm: pydFairnessConsiderations



class pydModelCard(BaseModel):
    """This section provides a general, high-level description of the model.

    Attributes:
        name: The name of the model.
        overview: A description of the model card.
        documentation: A more thorough description of the model and its usage.
        owners: The individuals or teams who own the model.
        version: The version of the model.
        licenses: The license information for the model. If the model is licensed
        for use by others, include the license type. If the model is not licensed
        for future use, you may state that here as well.
        references: Provide any additional links the reader may need. You can link
        to foundational research, technical documentation, or other materials that
        may be useful to your audience.
        citations: How should the model be cited? If the model is based on published
        academic research, cite the research.
        path: The path where the model is stored.

    Source: https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/model_card.py#L131
    """
    #model_config = ConfigDict(from_attributes=True)
    model_details : pydModelDetails
    versioning: pydVersion
    #considerations: pydConsiderations
    #License: pydLicense
    #Reference: pydReference 
    #Citation: pydCitation 
    interface: pydModelDataInterface 

# landing page on assessment
class pydAssessmentLandingPage(BaseModel):
  select_assessment_mode: EnumRAIAPage1Choice = Field(..., description="Choose the assessment option for current job.") 


class pydRAIIA_ProjectSummary_Background(BaseModel):
  project_name: str = Field(..., format="multi-line", description="Name of the AI project.")
  business_segment: str = Field(..., format="multi-line", description="Which segment of business is the AI project for.")
  project_start_date: datetime.date = Field(
        datetime.date.today(),
        description="When did the project start?",
    )  
  ai_system_launch_date: datetime.date = Field(
        datetime.date.today(),
        description="When was/will the AI system launched?",
    )
  region: str = Field(..., description="region where the AI system is deployed.")
  responsible_person: str = Field(..., description="Name of the person responsible for the AI system.")

class pydRAIIA_ProjectSummary_PotentialRisksSummary(BaseModel):
  legal_risk: str = Field(..., format="multi-line", description="Legal aspect of Risks.")
  reputational_risk: str = Field(..., format="multi-line", description="Reputational aspect of Risks.")
  ethical_risk: str = Field(..., format="multi-line", description="Ethical aspect of Risks.")
  environmental_risk: str = Field(..., format="multi-line", description="Environmental aspect of Risks.")
  

class pydRAIIA_ProjectSummary_Summary(BaseModel):
  high_level_technical_and_functional_overview: str = Field(..., format="multi-line", description="Overview of the AI project.")
  business_driver_and_context: str = Field(..., format="multi-line", description="Main driver for the business")
  external_data_sources_and_data_sets: str = Field(..., format="multi-line", description="Descriptions of external datasets used to train the AI model.")
  internal_data_sources_and_data_sets: str = Field(..., format="multi-line", description="Descriptions of internal datasets used to train the AI model.")
  summary_of_potential_risks: pydRAIIA_ProjectSummary_PotentialRisksSummary 
  external_related_documents: str = Field(..., format="multi-line", description="References to applicable Documents.")
  governance_model: str = Field(..., format="multi-line", description="The Governance Framework of the AI project.")
  project_team: str = Field(..., format="multi-line", description="The team members of the AI project.") 

class pydRAIIA_ProjectSummary(BaseModel):
  background: pydRAIIA_ProjectSummary_Background
  summary: pydRAIIA_ProjectSummary_Summary
  
class pydRAIIA_KeyfactorTemplate(BaseModel):
  answer: str = Field(..., format="multi-line", description="Answer to the question above")
  #predicted_risk : EnumRAIARiskLevel = Field(..., description="Choose the self-assessment risk level") 
  predicted_risk : int = Field(0, ge=0, le=5, multiple_of=1, description="Choose the self-assessment risk level. 0:No Risk, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High Risk.")

class pydRAIIA_AIEthicsPrinciplesTemplate(BaseModel):
  whether_or_how_the_solution_addresses_the_factor : str = Field(..., format="multi-line", description="Answer to the question above")
  #risk_rating : EnumRAIARiskLevel = Field(..., description="risk rating before mitigation") 
  risk_rating : int = Field(0, ge=0, le=5, multiple_of=1, description="risk rating before mitigation. 0:No Risk, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High Risk.") 
  mitigation_measures : str = Field(..., format="multi-line", description="elaborate your measures to mitigate the risk")
  #revised_risk_rating : EnumRAIARiskLevel = Field(..., description="risk rating after mitigation") 
  revised_risk_rating : int = Field(0, ge=0, le=5, multiple_of=1, description="risk rating after mitigation. 0:No Risk, 1:Very Low, 2:Low, 3:Medium, 4:High, 5:Very High Risk.")


KEYFACTOR_QUESTIONS = [
  #Context
  "Describe the context in which the AI system is used or deployed.",
  "Will the AI system be used in a public facing environment?",
  "What is the target market, industry or sector for the AI system?",
  #Law
  "Do the jurisdiction(s) in which the AI Solution will be deployed have data protection laws or regulation that are applicable to its use?",
  "Does the jurisdiction(s) in which the Project will take place abide by rule of law principles?",
  "Does this jurisdiction have antidiscrimination laws?",
  "What are the main regulatory requirements relevant to the use and deployment of the AI System within the targeted market, industry or sector?",
  "Will the AI System be used across legal jurisdiction borders (whether they be across federal states or national borders)?",
  "What are the main ethical concerns relevant to the use and deployment of the AI System for the targeted market, industry or sector?",
  #HumanOVersight
  "Will the AI System make or participate in making decisions with material impacts on individuals or society?",
  "What is the expected degree of autonomy of the AI System? Will, for instance, human operators or decision-makers have oversight on individual AI decisions, if any?",
  "How frequently will there be human oversight over the operation of the AI System?",
  "What measures would be taken to avoid automation bias or anchoring to the AI System?",
  "What will be the Organisation's degree of control and responsibility over the finalized AI System?",
  #StakeHolders - rights
  "Who will be the main stakeholders affected by the AI System?",
  "Who are the expected contributing third parties?",
  "What individual rights and interests will be at stake as a consequence of the use of the AI System?",
  "Are those rights fundamental or human rights?",
  #DataRpivacy
  "What is the type and origin of the data that will be used to train the AI System?",
  "Will the training data include personal information?",
  "If personal information are used in the context of the AI System, who are the data subjects?",
  "What is the level of sensitivity of the data in term of privacy?",
  #Explanability
  "What are the technical characteristics of the AI System that could influence the explainability and auditability of the algorithm?",
  "Can the results of the AI System be explained in humanly understandable terms?"
]

KEYFACTOR_RISK_CONTEXT = [
  #Context
  "The more people the system will interface with, the higher the risk is.",
  "The more people the system will interface with, the higher the risk is.",
  "The risk is relative to the impact to livelihoods and how many people will be impacted. For example, if the AI system is deployed on healthcare or military system, the risk is 5. If entertainment, risk is 1.",
  #Law
  "The exitance of more laws and regulations implies higher risk.",
  "The exitance of more laws and regulations implies higher risk.",
  "The exitance of more laws and regulations implies higher risk.",
  "The exitance of more regulatory requirements implies higher risk.",
  "Usage across federal state is risk 3. Across national border is risk 5. Not crossing border is risk 0.",
  "The more concerns, the higher is the risk.",
  #HumanOVersight
  "If it makes decision that impacts the society, risk is 5. If it impacts individuals, risk is 3. Otherwise risk is low.",
  "The less oversight from human, the higher is the risk. If no oversight at all, risk is 5.",
  "Risk is inversely proportianl to the frequency. If never the risk is 5."
  "More relevant measures given implies lower risk. Without any appropriate measure the risk is 5.",
  "More degree of control over the AI system implies lower risk. Without any control the risk is 5.",
  #StakeHolders - rights
  "The more stakeholders affected, the higher is the risk.",
  "The more third parties involved, the higher is the risk.",
  "The more rights will be impacted, the higher is the risk",
  "If it impact human rights, risk is 5. If fundamental rights, risk is 3. Otherwise, risk is 0.",
  #DataRpivacy
  "If the source of data potentially leaks sensitive info such as personal data, national security etc, the risk is 5",
  "If the answer is affirmative, the risk is 5",
  "The risk is relative to the population size of data subjects",
  "The risk is relative to the sensitivity of data",
  #Explanability
  "The clearer and more details given in the answer, the less is the risk. If no detail is given, risk is 5",
  "If the answer is a firm negative, the risk is 5, otherwise, the more explainability feature the less is the risk"
]

class pydRAIIA_KeyfactorContext(BaseModel):
  describe_the_context: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[0])
  public_facing: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[1])
  target: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[2])

class pydRAIIA_KeyfactorLaws(BaseModel):
  data_protection: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[3]) 
  rule_of_law: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[4])
  antidiscrimination: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[5])
  regulatory_requirements: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[6])
  cross_border_jurisdiction: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[7])
  ethical_concerns: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[8])

class pydRAIIA_KeyfactorHumanOversight(BaseModel):  
  material_impact: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[9]) 
  degree_of_autonomy: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[10]) 
  frequency_of_human_oversight: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[11])
  automation_bias_avoidance: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[12]) 
  control: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[13]) 

class pydRAIIA_KeyfactorStakeHolders(BaseModel): 
  stakeholders: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[14]) 
  third_parties: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[15]) 
  individual_rights_and_interests: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[16]) 
  fundamental_or_human_rights: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[17])  

class pydRAIIA_KeyfactorDataPrivacy(BaseModel):  
  origin_of_data: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[18]) 
  privacy_in_data: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[19]) 
  data_subjects: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[20]) 
  privacy_sensitivity: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[21]) 

class pydRAIIA_KeyfactorExplainability(BaseModel): 
  factors_to_explainability: pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[22]) 
  results_explainability:  pydRAIIA_KeyfactorTemplate = Field(..., description=KEYFACTOR_QUESTIONS[23]) 

class pydRAIIA_Keyfactor(BaseModel):
  context: pydRAIIA_KeyfactorContext
  laws: pydRAIIA_KeyfactorLaws
  stakeholders: pydRAIIA_KeyfactorStakeHolders
  human_oversight: pydRAIIA_KeyfactorHumanOversight
  data_privacy: pydRAIIA_KeyfactorDataPrivacy
  human_understandable_ai: pydRAIIA_KeyfactorExplainability

FAIR_QUESTIONS = [
  #1
  "Is the use of the AI System voluntary, incentive-based or compulsory?",
  #2
  "Is the AI System following a deterministic approach as opposed to a probabilistic model?",
  #3
  "Is the AI System making automated decisions affecting the rights and interests of individuals or businesses?",
  #4
  "Does the Organisation understand the lineage of data (where the data originally came from, how it was collected, curated and moved within its Business Unit/Division, and how its accuracy is maintained over time)? Consider keeping a data provenance record.",
  #5
  "Is the data high quality data?",
  #6
  "Is the data used for the training of the AI System representative of the population about which the AI System will make decisions (data accuracy, data quality and data completeness)?",
  #7
  "Does the Organisation have an established and robust selection process in relation to the datasets training the AI System? For example, are there minimum requirements as to the diversity and quality of the datasets used?",
  #8
  "Does the AI System use different datasets for training, testing and validation?",
  #9
  "Did the training process tried to minimise inherent biases like selection bias, wieghting bias, measurement bias, and other biases?",
  #10
  "Is there rigorous testing of the AI System, both before use and periodically afterwards, to ensure that there is no disparate impact on a protected class of individuals?",
  #11
  "How are “edge cases” managed by the AI System?",
  #12
  "Does the Organisation have in place a system to respond to and resolve situations in which the AI System produces discriminatory or unfair outcomes?",
  #13
  "What methodologies have been applied and used in the training of the AI System?",
  #14
  "Does the AI System have a fixed learning phase followed by a static use phase or does it continuously improve? If the latter, how are improvements filtered for bias, quality, etc.?",
  #15
  "What are the risks of bias existing or occurring in the algorithm, the training data, the human designers and developers, and end-users?",
  #16
  "What are the reputational risks for the Organisations of the AI System making biased automated decisions?"
]  


# AI assisted Risk Rating

FAIR_RISK_CONTEXT = [
  #1
  "If the AI system is compulsory, risk is 5. If it is voluntary, risk is 1. Icentive-based, risk is 3.",
  #2
  "Probablistic model makes it harder to evaluate fairness and discrimination than a deterministic model, so the risk should be higher for probabilistic models.",
  #3
  "If the AI is making decision that affects the rights and interest of individuals or businesses, the risk is high",
  #4
  "If the answer provides good description on its data governance or data provenance record, then the risk is very low.",
  #5
  "If the answer describes traits of good quality data considering aspects in source, governance and etc, the risk is very low.",
  #6
  "The risk is inversely proportional to the coverage of the training data to its target user and its completeness.",
  #7
  "The risk is inversely proportional to the description of a robust selection process provided in the answer.",
  #8
  "If there are seperate datasets for training, testing and validation, the risk is zero. If there is no testing dataset, the risk is very high.",
  #9
  "If the answer is positive and provides good description of what effort has been taken to minimise the bias, risk is very low. If the answer is negative, risk is very high.",
  #10
  "The risk rating would be very low if the answer implies very rigorous and frequent testing of the AI system after deployment, and gets higher if the test and validation is getting less frequent or less rigorous.",
  #11
  "Risk rating is very low when there is good mechanism in place to handle edge-cases. Very high if there is none.",
  #12
  "The risk rating is inversey proportional to the system the organization has. A good system implies very low risk. Simple, bad or no system implies high or very high risk.",
  #13
  "If the organisation put extra effort in checking the training data for potential biases, validate the AI model output for discrimination and etc, risk rating is very low.",
  #14
  "The risk rating would be low if the organization has continous bias detection and filtering mechanism for continously improved AI system. For AI with static learning phase, if the user described a filtering mechanism in his answer the risk will be low as well.",
  #15
  "The risk rating is relative to the exitence or occurance of bias in the the algorithm, the training data, the human designers and developers, and end-users.",
  #16
  "Risk rating is relative to the magnitude of the reputational risk the Organisations might face."
  ""

]




class pydRAIIA_FairnessAssessment(BaseModel): 
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[0]) 
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[1]) 
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[2]) 
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[12])
  risk_factor_14: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[13])
  risk_factor_15: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[14])
  risk_factor_16: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=FAIR_QUESTIONS[15])

RELIABILITY_QUESTIONS = [
  #1
  """Is there a clearly defined set of relevant ethical and moral principles in place on the basis of which the AI System is intended to operate, such taking into account all relevant circumstances?
      \nHave all local standards been identified and taken into account e.g. in relation to geographical, religious and/or social considerations and traditions? 
      \nAre the underpinning ethical and moral principles periodically validated to ensure on-going accurateness, starting with a validation prior to the design and development of the AI System?""",
  #2
  """Have ethical and moral appropriateness considerations been translated into (technical and/or functional) boundaries affecting the outcome of the AI System’s use (e.g. its decision-making powers)? What is the impact of this on the general accuracy of the outcome of the AI System’s use?""",
  #3
  """Have safety and reliability risk scenarios been identified, both for the AI System’s users and beyond (e.g. potentially indirectly affected stakeholders or society at large), including associated risk metrics and risk levels, in relation to: 
      \na) the quality and performance of the AI System itself (e.g. design faults, technical defects, low level of accuracy, unintended self-learning capabilities);
      \nb) the data and assumptions used to develop and train the AI System (e.g. preventing data that are not up-to-date, incomplete and/or non-representative);
      \nc)  any possible (harmful) use of the AI System or the outcome thereof (e.g. over-reliance, human attachment, addictive user behaviour and manipulation of user behaviour), including any malicious, inappropriate or unintended (dual) use; and
      \nd) the safety and reliability expectations of the users and their level of sophistication.""",
  #4
  """Has a definition been set of what is considered to be a safe and reliable AI System, and is this definition commonly used and implemented throughout the full lifecycle of design, development, deployment, operation and use of the AI System? 
      \nHave quantitative analysis or metrics been applied to measure and test the applied definition?
      \nAre there regulatory requirements that impact the above definition of safety and reliability (e.g. medical devices regulations)?""",
  #5
  """Have clear fault tolerance requirements been set that are considered acceptable in relation to the intended outcome of the AI System’s use? If yes, what is the basis for setting these fault tolerance requirements (e.g. a legacy solution that the AI System will be replacing)?""",
  #6
  "Has the AI System been assessed to determine whether (and if so, the extent to which) it is also safe for, and can be reliably used by, those with special needs or disabilities or those at risk of exclusion?",
  #7
  "Are all safety and reliability considerations as addressed in aforementioned questions expressed in the design and development documentation in sufficient detail?",
  #8
  "How is the AI System’s testability and auditability facilitated?",
  #9
  "Is the testing procedure aligned to the appropriate levels of safety and reliability as needed, taking into account the safety and reliability considerations expressed in the design and development documentation? Does the testing procedure also accommodate for testing of the AI System in “edge cases” (use scenarios that are unlikely to occur but are nonetheless possible)?",
  #10
  "Has a “pilot” deployment been considered to enable testing and refining the operation of the AI System and to expedite the completion of the AI System improve its safety and reliability? If yes, has this pilot been limited in time and users, have users been informed about the specifics of the pilot, and is it possible to safely abort upon short notice?",
  #11
  "Are there any specific human oversight and control measures in place that reflect the safety and reliability risks of the AI System, given the degree of self-learning and autonomous features of the AI System?",
  #12
  "What procedures are in place to ensure the explainability of the AI System’s decision-making process during operation?",
  #13
  "How is the ongoing auditing of the AI System’s safety and reliability organised and facilitated, internally as well as by independent third parties? Aside from exception reporting, does this also include failure analysis to determine causes or fixes for any problems? Is safety audited separately from reliability?",
  #14
  """Are users informed on:
    \na) the (technical and/or functional) boundaries implemented to affect the outcome of the AI System’s use;
    \nb) the potential safety and reliability risks of the AI System to the users (e.g. the level of accuracy of the AI System to be expected by users); and
    \nc) the duration of coverage and schedules timeframes for security and other updates to improve the safety and/or reliability of the AI System?""",
  #15
  "Contrary to Q14, does the AI System serve primarily to empower workers (by providing them with effective tools, skills or knowledge to assist them in the workplace)?",
  #16
  "Are there environmental risks associated with the AI System (including excessive pollution, or excessive energy or non-renewable resource consumption)?",
  #17
  "Contrary to Q16, does the AI System facilitate the environmentally and energy-efficient use of resources?",
  #18
  "Are there military or lethal uses for the proposed AI System? If so, answer Q19 and Q20 as appropriate. If no, go to Q21.",
  #19
  "Is there a process in place to continuously measure and assess safety and reliability risks in accordance with the risk metrics and risk levels defined in advance for each specific use case?",
  #20
  "Are there procedures and/or measures in place that ensure comprehensive and transparent investigation of adverse, unanticipated and/or undesirable alterations to or outcomes of the AI System, in particular in the event of resulting harm to the safety of its users or beyond (e.g. to society at large), and that mitigate any risks of such resulting harm occurring?",
  #21
  "Is there a mechanism in place that allows for designers, developers, users, stakeholders and third parties to (anonymously) flag/report vulnerabilities and other issues related to the safety and reliability of the AI System?",
  #22
  "Are there tested failsafe fall-back plans to address the AI System’s errors of whatever origin, including governance procedures to trigger them?",
  #23
  "Is the AI System designed in such a way (e.g. by including a ‘stop button’) that it can safely and elegantly abort the deployment and/or operation of the AI System when needed without catastrophic results for the users and beyond?",
  #24
  "How are the results of all risk assessment, risk management and risk control procedures in relation to safety and reliability of the AI System factored into necessary or desirable alterations of (the design of) the AI System? How is this process documented?"
]


RELIABILITY_RISK_CONTEXT = [
  #1
  """The clearer and more details user provides in the answer, the lower is the risk.
     If the AI System has a well-defined and comprehensive set of ethical and moral principles that consider all relevant circumstances, including local standards, and these principles are periodically validated, the risk rating would be 0-2.
     If the principles are somewhat incomplete or not thoroughly validated, the risk rating would be 3-4.
     If the principles are poorly defined, do not adequately consider local standards, or lack validation, the risk rating would be 5.""",
  #2
  """The clearer and more details user provides in the answer, the lower is the risk. 
     If ethical and moral considerations have been thoroughly translated into technical and/or functional boundaries, and these boundaries do not significantly impact the accuracy of the AI System's outcome, the risk rating would be 0-2.
     If the boundaries are somewhat incomplete or have a moderate impact on accuracy, the risk rating would be 3-4.
     If the boundaries are poorly defined, do not adequately reflect ethical and moral considerations, or significantly reduce accuracy, the risk rating would be 5.""",
  #3
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #4
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #5
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #6
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #7
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #8
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #9
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #10
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #11
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #12
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #13
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #14
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #15
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #16
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #17
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #18
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #19
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #20
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #21
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #22
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #23
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #24
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
]

class pydRAIIA_ReliabilityAssessment(BaseModel):
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[0])
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[1])
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[2])
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[12])
  risk_factor_14: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[13])
  risk_factor_15: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[14])
  risk_factor_16: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[15])
  risk_factor_17: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[16])
  risk_factor_18: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[17])
  risk_factor_19: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[18])
  risk_factor_20: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[19])
  risk_factor_21: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[20])
  risk_factor_22: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[21])
  risk_factor_23: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[22])
  risk_factor_24: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=RELIABILITY_QUESTIONS[23])


PRIVACY_QUESTIONS = [
#1
"""Consider if the data is provided by the individual (originated in direct action taken by the individual) and whether:
                                                             \n* The data is initiated (the product of individuals taking an action that begins a relationship) 
                                                             \n* The data is transactional (created when the individual is involved in a transaction) 
                                                             \n* The data is posted (created when individuals proactively express themselves) (See note 3 below.)""",
#2
"""Consider if the data is observed (created as the result of individuals being observed and recorded), whether:
                                                             \n* The data is engaged (instances in which individuals are aware of observation at some point in time)
                                                             \n* The data is not anticipated (instances in which individuals are aware there are sensors but have little awareness that sensors are creating data pertaining to the individuals)
                                                             \n* The data is passive (instances in which it is very difficult for the individuals to be aware they are being observed and data pertaining to observation of them is being created)""",
#3
"""Consider if the data is derived (created in a mechanical fashion from other data and becomes a new data element related to the individual), whether:
                                                             \n* The data is computational (creation of a new data element through an arithmetic process executed on existing numeric elements) 
                                                             \n* The data is notational (creation of a new data element by classifying individuals as being part of a group based on common attributes shown by members of the group)""",
#4
"""Consider if the data is inferred (product of a probability-based analytic process), whether:
                                                             \n* The data is statistical (the product of characterization based on a statistical process)
                                                             \n* The data is advanced analytical (the product of an advanced analytical process)""",
#5
"""How was the data used by the AI System collected and stored? Was the data transferred by third parties or will the data be transferred to third parties?
                                                             \n* Consider whether preprocessing activity has been done on the data before the analysis and whether it would have affected the accuracy and appropriateness of individuals.""",
#6
"""Who were the data subjects? What type of information was collected about them? What is the scope of the consents obtained?""",
#7
"""Is sensitive data collected? If so, are there higher standards being adopted for protection of this kind of data?""",
#8
"""Beyond the data subjects’ privacy, may the privacy of an identified group be at risk? (See note 4 below.)""",
#9
"""Are there viable alternatives to the use of personal information (e.g. anonymization or synthetic data)? If so, what mechanisms/techniques are implemented to prevent from re-identification?""",
#10
"""Are there procedures for reviewing data retention and performing destruction of data used by the AI System? Are there oversight mechanisms in place?""",
#11
"""What is the nature of the Organisation’s relationship with the data subjects? How much control will they have? Would they expect you to use their data in this way? (See note 5 below.)""",
#12
"""Do they include children or other vulnerable groups? Are there prior concerns over this type of processing or security flaws?""",
#13
"""What is the Organisation’s lawful basis for processing personal information? What measures does the Organisation take to ensure compliance? """
]

PRIVACY_RISK_CONTEXT = [
  #1
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #2
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #3
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #4
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #5
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #6
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #7
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #8
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #9
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #10
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #11
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #12
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #13
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
]

class pydRAIIA_PrivacyAssessment(BaseModel):
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[0])
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[1])
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[2])
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=PRIVACY_QUESTIONS[12])

ACCOUNTABILITY_QUESTIONS = [
#1
"""Is this AI System an expansion of a previous activity? If yes, determine whether a previous assessment has been done. If a previous assessment has been done, what has changed in this data activity and why (refer to previous assessment)? """,
#2
"""How experienced with tech projects is the team that will develop the AI System? """,
#3
"""What is the level of internal support, including financial, for the AI System? """,
#4
"""Who will be accountable within the organisation with regards to the AI System? Is there a central coordinating body? Who will be accountable within the organisation upon failure of the AI System, or upon production of adverse outcomes for its users? """,
#5
"""Will the staff be trained to use the AI System? Are the relevant personnel and/or departments fully aware of their roles and responsibilities?
                                                             \n* This inquiry should account for the different types of staff and the different layers of personnel involved in the design of the AI System (e.g. management/oversight in addition to programming levels).""",
#6
"""What elements of the training and development “supply chain” have been outsourced? If handed off to a third party, are their services subject to the same levels of quality control as the Organisation?""",
#7
"""What are the roles played by the Organisation within the AI System pipeline (end-user, developer, data provider, etc.)?""",
#8
"""What will be the relation of the Organisation with end users once the AI System developed reaches the market (for instance, is AI System sold as a product or as a Software-as-a-Service)?""",
#9
"""To what extent does the AI System rely on third party data/systems input? How accountable are those third-party dependencies?""",
#10
"""What is the maximum degree of autonomy that the AI System can reach? """,
#11
"""Identify all stakeholders that are affected by the AI System.""",
#12
"""How will the internal use of the AI System by the Organisation affect the roles and tasks of employees?""",
#13
"""Does the Organisation provide a method for individuals to access and correct personal information used in the AI System? How does this change if the data isn’t deemed to be personal data (i.e. anonymized and not re-identifiable) but yet relates to a human? """,
#14
"""Does the AI System provide functionality allowing the user to “turn off” the app for a limited time? """,
#15
"""Does the AI System conform to industry or sector specific regulations given its deployment capabilities and its data source? (e.g. consumer protection, banking, health sector) """,
#16
"""Is there an independent commissioner committed to the review and control of such AI Systems? (e.g. governmental agency, designated official) """,
#17
"""Is a Privacy Policy available? """,
#18
"""Are the principles of necessity, proportionality and data minimization fully integrated? """,
#19
"""What privacy by design measures have been implemented? """,
#20
"""Are personal data that are being collected by the AI System used for any secondary purposes (after the “sunset” of the AI System)? Are secondary uses of data compatible with initial purposes, if any? """,
#21
"""How are transfers of data of the AI System outside of the EU/national/regional frontier organized?  """,
#22
"""Have external QA/QC control methodologies been observed in the creation of the AI System (i.e. ISO 9001)? """,
#23
"""How will the AI model training and selection process be managed? """,
#24
"""Consider maintenance, monitoring, documentation and review of the AI models that have been deployed. """,
#25
"""Consider the various degrees of human oversight in the decision-making process:
                                                              \na) Human-in-the-Loop: This model suggests that human oversight is active and involved, with the human retaining full control and the AI only providing recommendations or input. Decisions cannot be exercised without affirmative actions by the human, such as a human command to proceed with a given decision.
 	                                                            \nb) Human-out-of-the-Loop: This model suggests that there is no human oversight over the execution of decisions. AI has full control without the option of human override.
                                                              \nc) Human-over-the-Loop: This model allows humans to adjust parameters during the execution of the algorithm.""",
#26
"""What are the rights and interests at stake when the AI System makes an automated decision?"""
]

ACCOUNTABILITY_RISK_CONTEXT = [
  #1
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #2
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #3
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #4
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #5
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #6
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #7
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #8
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #9
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #10
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #11
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #12
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #13
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #14
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #15
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #16
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #17
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #18
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #19
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #20
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #21
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #22
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #23
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #24
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #25
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #26
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
]

class pydRAIIA_AccountabilityAssessment(BaseModel):
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[0])
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[1])
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[2])
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[12])
  risk_factor_14: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[13])
  risk_factor_15: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[14])
  risk_factor_16: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[15])
  risk_factor_17: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[16])
  risk_factor_18: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[17])
  risk_factor_19: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[18])
  risk_factor_20: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[19])
  risk_factor_21: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[20])
  risk_factor_22: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[21])
  risk_factor_23: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[22])
  risk_factor_24: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[23])
  risk_factor_25: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[24])
  risk_factor_26: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=ACCOUNTABILITY_QUESTIONS[25])
  

TRANSPARENCY_QUESTIONS = [
  #1
  """Has a governance methodology been implemented to apply transparency and explainability by design principles throughout the development lifecycle? """,
  #2
  """Have developmental and operational policies procedures and controls been implemented pursuant to such methodology? """,
  #3
  """Have internal controls been developed pursuant to such policies and procedures? """,
  #4
  """How did the selection of the system architecture and algorithmic model take transparency and explainability into account? """,
  #5
  """How did the selection of data sets to train and test the AI System take transparency and explainability into account? """,
  #6
  """Do terms and conditions apply to those individuals who may wish to access and use the AI System (“Terms of Use”)? """,
  #7
  """Are the Terms of Use clearly and prominently displayed? """,
  #8
  """Are there any limitations on accessing the Terms of Use (e.g. a registration process)? """,
  #9
  """What steps were taken to ensure the Terms of Use are accurate? """,
  #10
  """What steps were taken to ensure the Terms of Use are objectively clear and readily understandable to a layperson? """,
  #11
  """Do the Terms of Use vary based upon the level of sophistication or other attributes of a user? If so, how? """,
  #12
  """Do the Terms of Use apply a layered disclosure approach to allow interested individuals the ability to obtain more information about the AI System? """,
  #13
  """Do the Terms of Use provide meaningful information regarding the fact that an AI System is being used in a decision-making process? If so, how? """,
  #14
  """Do the Terms of Use provide meaningful information regarding the intended purpose(s) of the AI System? If so, how? """,
  #15
  """Do the Terms of Use provide meaningful information regarding the types of data sets that are used and generated by the AI System? If so, how? """,
  #16
  """Do the Terms of Use provide meaningful information regarding whether and to what extent the decision-making process may include human participation? If so, how? """,
  #17
  """Are prior versions of the Terms of Use publicly available? """,
  #18
  """Is there a process to periodically review and update the Terms of Use? """,
  #19
  """Is there a process to periodically assess whether users understand the Terms of Use? """,
  #20
  """How are the results of the AI System made available to users? """,
  #21
  """When are the results of the AI System made available to users? """,
  #22
  """At such time, what information is provided regarding the algorithmic logic of the AI System? """,
  #23
  """At such time, what information is provided to understand the decision/outcome? """,
  #24
  """At such time, what information is provided regarding how to contest the decision/outcome? """,
  #25
  """At such time, what information is provided regarding the traceability or auditability of the AI System? """,
  #26
  """At such time, what information is provided regarding the testing methods of the AI System? """,
  #27
  """Are any other disclosures made with respect to the transparency and explainability of the AI System (e.g. videos, icons, symbols, white papers, dashboards, or counterfactual interfaces)? """,
  #28
  """Does the disclosure of any information listed in this section change depending on the nature of the data involved (e.g. if sensitive personal data is used by the AI System)? If so, how? """,
  #29
  """Does such disclosure change depending on the lack of human participation in the decision-making? If so, how? """,
  #30
  """Does such disclosure change depending on the result of the decision and its consequences for the user (e.g. if legal or human rights are materially affected)? If so, how? """,
  #31
  """Is the AI System periodically audited or assessed with respect to transparency and explainability, either internally or by an independent third party? """

]


TRANSPARENCY_RISK_CONTEXT = [
  #1
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #2
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #3
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #4
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #5
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #6
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #7
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #8
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #9
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #10
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #11
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #12
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #13
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #14
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #15
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #16
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #17
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #18
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #19
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #20
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #21
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #22
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #23
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #24
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #25
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #26
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #27
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #28
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #29
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #30
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #31
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
]

class pydRAIIA_TransparencyAssessment(BaseModel):
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[0])
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[1])
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[2])
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[12])
  risk_factor_14: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[13])
  risk_factor_15: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[14])
  risk_factor_16: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[15])
  risk_factor_17: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[16])
  risk_factor_18: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[17])
  risk_factor_19: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[18])
  risk_factor_20: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[19])
  risk_factor_21: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[20])
  risk_factor_22: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[21])
  risk_factor_23: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[22])
  risk_factor_24: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[23])
  risk_factor_25: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[24])
  risk_factor_26: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[25])
  risk_factor_27: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[26])
  risk_factor_28: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[27])
  risk_factor_29: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[28])
  risk_factor_30: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[29])
  risk_factor_31: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=TRANSPARENCY_QUESTIONS[30])


HAPPINESS_QUESTIONS = [
  #1
  """Is the AI System consistent with the ethical principles, values, standards, policies and/or code of conduct of the Organisation? """,
  #2
  """Are there any potential reputational and material risks attached to the AI System for the Organisation? """,
  #3
  """Is there a risk that use of the AI System will violate any fundamental human rights (such as rights of freedom, free expression, non-discrimination)? """,
  #4
  """Does the AI System raise risks to human agency (such as self-determination, choice, free will, unfettered decision making, and the ability to self-regulate one’s own affairs) in respect of the intended end user audience or other ecosystem stakeholders? """,
  #5
  """Does the AI System raise risks to human autonomy (such as freedom of movement and travel; data portability) in respect of the intended end user audience or other ecosystem stakeholders? """,
  #6
  """Is there a risk(s) that the AI System could generate confusion as to whether or not the user is interacting with a human or an AI System? """,
  #7
  """Does the AI System involve surreptitious surveillance or excessive surveillance that might impose a danger to human agency and autonomy (such as encouraging self-censorship or limiting freedom of expression or assembly)? """,
  #8
  """Does the AI System promote over-reliance, dependency, addiction or attention deficit? """,
  #9
  """Does the AI System raise risks of psychological and behavioural manipulation, coercion or excessive nudging? """,
  #10
  """Does the AI System hinder the user’s ability to make informed decisions? """,
  #11
  """Contrary to Q9, does the AI System empower the user? """,
  #12
  """Is there a risk that the AI System will promote the spread of false or misleading information? """,
  #13
  """Is there a risk that the AI System will promote the spread of hate speech, unlawful content or content which is potentially dangerous (physically, psychologically, or emotionally) to the end recipients/viewers of the content? """,
  #14
  """Are there employment-related risks associated with the AI System (such as material job loss or functionality that might detrimentally affect the quality of work experience)? """,
  #15
  """Contrary to Q14, does the AI System serve primarily to empower workers (by providing them with effective tools, skills or knowledge to assist them in the workplace)? """,
  #16
  """Are there environmental risks associated with the AI System (including excessive pollution, or excessive energy or non-renewable resource consumption)? """,
  #17
  """Contrary to Q16, does the AI System facilitate the environmentally and energy-efficient use of resources? """,
  #18
  """Are there military or lethal uses for the proposed AI System? If so, answer Q19 and Q20 as appropriate. If no, go to Q21. """,
  #19
  """In the case of military or lethal uses of the AI System: 
                                                              \n(a) Is the AI System fully autonomous? 
                                                              \n(b) is there a shutdown function triggered by designated personnel? 
                                                              \n(c) Is there effective human oversight in place? """,
  #20
  """In the case of military and lethal uses of the AI System: 
                                                              \n(a) is the AI System semi-autonomous? 
                                                              \n(b) Is there a shut down function triggered by designated personnel? 
                                                              \n(c) Is there effective human oversight in place? """,
  #21
  """May the AI System be deemed to be a medical device or any other qualification that could entail application of other regulations (e.g. medical secrecy) that could modify its ethical perception? """,
  #22
  """Is there a risk that the AI System could violate ethical principles of beneficence and non-maleficence? """,
  #23
  """Is there a risk that the AI System could have a negative impact on democratic and/or electoral processes? """,
  #24
  """Is there a risk that the AI System could have a negative impact on judicial judgment and/or processes, legal procedural due process and/or access to justice? """,
  #25
  """Is there a risk that the AI System could have a negative impact on learner pathways, assessment for attaining a qualification, assessment for a job or promotion, access to educational institutions and/or access to further learning opportunities? """,
  #26
  """Is there a risk that the AI System could select, classify, or categorize or seek to ascertain a level of assurance concerning individuals (or groups of individuals) in such a manner as to deny them access to a good or service (or promote too high a barrier of entry resulting in effective exclusion) which is unreasonable and unjustifiable? """
]

HUMANHAPPINESS_RISK_CONTEXT = [
  #1
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #2
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #3
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #4
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #5
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #6
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #7
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #8
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #9
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #10
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #11
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #12
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #13
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #14
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #15
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #16
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #17
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #18
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #19
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #20
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #21
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #22
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #23
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #24
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #25
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
  #26
  """The clearer and more details user provides in the answer, the lower is the risk. If the answer provided addresses all the concerns raised by the question then the risk is 1.""",
]

class pydRAIIA_HumanHappinessAssessment(BaseModel):
  risk_factor_1: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[0])
  risk_factor_2: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[1])
  risk_factor_3: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[2])
  risk_factor_4: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[3])
  risk_factor_5: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[4])
  risk_factor_6: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[5])
  risk_factor_7: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[6])
  risk_factor_8: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[7])
  risk_factor_9: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[8])
  risk_factor_10: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[9])
  risk_factor_11: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[10])
  risk_factor_12: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[11])
  risk_factor_13: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[12])
  risk_factor_14: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[13])
  risk_factor_15: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[14])
  risk_factor_16: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[15])
  risk_factor_17: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[16])
  risk_factor_18: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[17])
  risk_factor_19: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[18])
  risk_factor_20: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[19])
  risk_factor_21: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[20])
  risk_factor_22: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[21])
  risk_factor_23: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[22])
  risk_factor_24: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[23])
  risk_factor_25: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[24])
  risk_factor_26: pydRAIIA_AIEthicsPrinciplesTemplate = Field(..., description=HAPPINESS_QUESTIONS[25])









