from pydantic import BaseModel, Field, StringConstraints, ConfigDict
import datetime
from typing_extensions import Annotated
import dataclasses
from typing import Any, Dict, List, Optional, Union
from .enums import EnumCountry


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
    name: Annotated[str, StringConstraints(max_length=20)] = Field(..., description="The name of the model.")
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
  name: str = Field(..., description="The name of the version.")
  date: str = Field(..., description="The date this version was released.")
  diff: str = Field(..., description="The changes from the previous version.")

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
   model_api: str = Field(..., description="API endpoint for calling inference function of the model (URL).")
   data_api : str  = Field(..., description="API endpoint for sampling evaluation dataset, must adhere to specified format")

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
  limitations: str = Field(..., format="multi-line", description="What are the known limitations of the model? This may include technical limitations, or conditions that may degrade model performance.") 
  tradeoffs: str = Field(..., format="multi-line", description=" What are the known accuracy/performance tradeoffs for the model?") 
  ethical_considerations: str = Field(..., format="multi-line", description="What are the ethical risks involved in application of this model? For each risk, you may also provide a mitigation strategy that you've implemented, or one that you suggest to users.") 


class pydConsiderations2(BaseModel):
  target_users: str = Field(..., format="multi-line", description="Who are the intended users of the model? You might also include information about the downstream users you expect to interact with your model.") 
  feature_modalities:   


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
    Model : pydModelDetails
    #Owner: pydOwner 
    Version: pydVersion
    Considerations: pydConsiderations
    #License: pydLicense
    #Reference: pydReference 
    #Citation: pydCitation 
    Interface: pydModelDataInterface 