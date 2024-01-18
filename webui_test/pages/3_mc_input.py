import streamlit as st
from pydantic import BaseModel, Field, ConfigDict
import datetime
import streamlit_pydantic as sp
import model_card_toolkit as mctlib

#experimental modules
import dataclasses
from typing import Any, Dict, List, Optional, Union
from model_card_toolkit.model_card import (
    Citation, ConfidenceInterval, Considerations, Dataset, Graphic,
    GraphicsCollection, KeyVal, License, Limitation, ModelCard, ModelDetails,
    ModelParameters, Owner, PerformanceMetric, QuantitativeAnalysis, Reference,
    Risk, SensitiveData, Tradeoff, UseCase, User, Version, load_model_card
)

#experiments on rendering INput Output
st.set_page_config(
    page_title="Registering a Model Card",
    page_icon="🚀",
)


st.title("Registering A Model Card")

# First need to create a pydantic model equivalent of ModelDetails 

class pydModelDetails(BaseModel):
    """https://github.com/tensorflow/model-card-toolkit/blob/74d7e6d8d3163b830711b226491ccd976a2d7018/model_card_toolkit/model_card.py#L131
    """
    name: str = Field(..., description="The name of the model.")
    overview: str = Field(..., description="A description of the model card. of this")
    documentation: str = Field(..., description="A more thorough description of the model and its usage.")

class pydOwner(BaseModel):
  """The information about owners of a model.

  Attributes:
    name: The name of the model owner.
    contact: The contact information for the model owner or owners. These could
      be individual email addresses, a team mailing list expressly, or a
      monitored feedback form.
  """
  name: str = Field(..., description="The name of the model owner.")
  contact: str = Field(..., description="The contact information for the model owner or owners. These could be individual email addresses, a team mailing list expressly, or a monitored feedback form.")

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

class pydModelInterface(BaseModel):
   """How to interface with the model
   Attributes:
     api: API endpoint for calling inference function of the model 
   """
   api: str = Field(..., description="API endpoint for calling inference function of the model (URL).")


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
    Owner: pydOwner 
    Version: pydVersion
    License: pydLicense
    Reference: pydReference 
    Citation: pydCitation 
    Interface: pydModelInterface 

#or idea: https://github.com/LukasMasuch/streamlit-pydantic/blob/390a45aba7bf8caccc297c335715cc141db490af/src/streamlit_pydantic/ui_renderer.py#L1341
with st.form(key="pydantic_form"):
    input_model = sp.pydantic_input(key="mc_input_model", model=pydModelCard, group_optional_fields="expander")
    submit = st.form_submit_button(label="update")


