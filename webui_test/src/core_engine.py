import model_card_toolkit as mct
from model_card_toolkit.model_card import Owner
from model_card_toolkit.model_card import ModelDetails

class AssessmentEngine:
    def __init__(self):
        pass

    def validate_data(self):
        pass

    def run(self):
        # run
        pass

class ModelOwner(Owner):
    def __init__(self):
        self.UUID = 0
    
    def update_database(self):
        """
        Update owner info in database
        """
        pass

    def generate_id(self):
        """
        Generate a UUID for this company
        """
        pass

class Model(ModelDetails):
    def __init__(self):
        self.UUID = 0
        self.interface = "" #how to call a blackbox mode
        self.model_card = mct.ModelCard()

    def run_test(self):
        pass

    def generate_report(self):
        pass

    def load_report(self):
        pass

    def call_inference(self):
        pass