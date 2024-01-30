from typing import Any
import requests
#import fairlearn
from src.enums import EnumFeatureType
import json
import logging
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score
from fairlearn.metrics import (
    MetricFrame,
    count,
    false_negative_rate,
    false_positive_rate,
    selection_rate,
)
from model_card_toolkit.utils.graphics import figure_to_base64str #encode matplotlib figure to string that model card can accept


headers = {"Content-Type": "application/json"}

MAX_SIZE = 10000

class BACKEND_TEST:
    def __init__(self, *args: Any, **kwds: Any):
        self.logger = logging.getLogger(__name__)

        #ref https://docs.python.org/3/howto/logging.html#configuring-logging
        #self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)

        #
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d- %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        #handler.addLevelName('INFO', 'Info')
        #handler.addLevelName('WARNING', 'Warning')
        #handler.addLevelName('ERROR', 'Error')
        #handler.addLevelName('CRITICAL', 'Critical')
        

    def check_endpoints(self, ftype: str, endpoint: str) -> bool : 
        """check if all required endpoints are defined at API"""
        try:
            self.logger.info(ftype +" "+ endpoint)
            response = requests.get(f"{endpoint}/get_size")
            if response.status_code != 200:
                self.logger.warning("\'get_size\' endpoint validation failed!")
                return False
            else:
                self.feature_size = int(response.content)  #row count
            if ftype == EnumFeatureType.TAB.value:
                body = json.dumps([0])            
                response = requests.post(f"{endpoint}/sample", data=body, headers=headers)
                if response.status_code != 200:
                    self.logger.warning("\'sample\' endpoint validation failed!")
                    return False
                X = json.loads(response.content)["feature"]
                X = pd.DataFrame(X)
                self.feature_count = X.columns.size #column count
                response = requests.post(f"{endpoint}/predict", data=json.dumps(X.to_dict()), headers=headers)
                if response.status_code != 200:
                    self.logger.warning("\'predict\' endpoint validation failed!")
                    return False
            self.logger.info("endpoint validation passed")
            self.endpoint = endpoint
            return True
        except Exception as e:
            self.logger.warning(e)

    def fairness_assess(self):
        """
        refs:
            https://fairlearn.org/v0.10/quickstart.html#evaluating-fairness-related-metrics
            https://fairlearn.org/v0.10/api_reference/generated/fairlearn.metrics.MetricFrame.html#fairlearn.metrics.MetricFrame
            https://fairlearn.org/v0.10/auto_examples/plot_quickstart.html#sphx-glr-auto-examples-plot-quickstart-py
            graphics: https://www.tensorflow.org/responsible_ai/model_card_toolkit/examples/Standalone_Model_Card_Toolkit_Demo
        """
        if self.feature_size <= MAX_SIZE:
            idx = list(range(self.feature_size))
        else:
            import random
            whole_idx = list(range(self.feature_size))
            idx = random.sample(whole_idx, MAX_SIZE)
        idx = json.dumps(idx)
        try:
            response = requests.post(f"{self.endpoint}/sample", data=idx, headers=headers)
            if response.status_code != 200:
                self.logger.warning(f"\'sample\' failed with status {response.status_code}")
                return {}
            feature = json.loads(response.content)["feature"]
            feature = pd.DataFrame(feature) 
            label = json.loads(response.content)["label"]
            label = pd.DataFrame(label)
            sensitive = json.loads(response.content)["sensitive"]
            sensitive = pd.DataFrame(sensitive) 
            response = requests.post(f"{self.endpoint}/predict", data=json.dumps(feature.to_dict()), headers=headers)
            if response.status_code != 200:
                self.logger.warning(f"\'predict\' failed with status {response.status_code}")
                return {}
            predict = json.loads(response.content)
            predict = pd.DataFrame(predict)
            # from https://fairlearn.org/v0.10/auto_examples/plot_quickstart.html#sphx-glr-auto-examples-plot-quickstart-py
            metrics = {
                "accuracy": accuracy_score,
                "precision": precision_score,
                "false positive rate": false_positive_rate,
                "false negative rate": false_negative_rate,
                "selection rate": selection_rate,
                "count": count,
            }
            metric_frame = MetricFrame(
                metrics=metrics, y_true=label, y_pred=predict, sensitive_features=sensitive
            )
            fig = metric_frame.by_group.plot.bar(
                subplots=True,
                layout=[3, 2],
                legend=False,
                figsize=[7, 12],
                title="Fairness Assessment",
            )

            print("performance mf bygroup:\n", metric_frame.by_group)

            ## Customize plots with ylim
            #metric_frame.by_group.plot(
            #    kind="bar",
            #    ylim=[0, 1],
            #    subplots=True,
            #    layout=[3, 3],
            #    legend=False,
            #    figsize=[12, 8],
            #    title="Show all metrics with assigned y-axis range",
            #)

            ## Customize plots with colormap
            #metric_frame.by_group.plot(
            #    kind="bar",
            #    subplots=True,
            #    layout=[3, 3],
            #    legend=False,
            #    figsize=[12, 8],
            #    colormap="Accent",
            #    title="Show all metrics in Accent colormap",
            #)

            ## Customize plots with kind (note that we are only plotting the "count" metric here because we are showing a pie chart)
            #metric_frame.by_group[["count"]].plot(
            #    kind="pie",
            #    subplots=True,
            #    layout=[1, 1],
            #    legend=False,
            #    figsize=[12, 8],
            #    title="Show count metric in pie chart",
            #)

            # Saving plots
            #fig = metric_frame.by_group[["count"]].plot(
            #    kind="pie",
            #    subplots=True,
            #    layout=[1, 1],
            #    legend=False,
            #    figsize=[12, 8],
            #    title="Show count metric in pie chart",
            #)
            #fig[0][0].figure.savefig("metricFrame.png")

            return metric_frame.by_group, figure_to_base64str(fig[0][0].figure)


        except Exception as e:
            self.logger.warning(e)



