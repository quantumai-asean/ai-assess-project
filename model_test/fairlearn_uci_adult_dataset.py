from fairlearn.datasets import fetch_adult
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os
from fastapi import FastAPI
import uvicorn
from typing import List


# taken from https://fairlearn.org/v0.10/quickstart.html#loading-the-dataset

data = fetch_adult(as_frame=True)
X = pd.get_dummies(data.data)
y_true = (data.target == '>50K') * 1
sex = data.data['sex']
model_path = 'uci_adult.pkl'
cwd = os.getcwd()


def train_model():    
    classifier = DecisionTreeClassifier(min_samples_leaf=10, max_depth=4)
    classifier.fit(X, y_true)

    # Save the model
    with open(os.path.join(cwd,model_path), 'wb') as f:
        pickle.dump(classifier, f)

    return classifier

def load_model():
    # Load the model from disk
    classifier = pickle.load(open(os.path.join(cwd,model_path), 'rb'))
    return classifier

# fastapi request: https://fastapi.tiangolo.com/tutorial/body/

app = FastAPI()

    
if os.path.exists(os.path.join(cwd,model_path)):
    #print("path exists")
    classifier = load_model()
else:
    #print("file doesnt exist")
    classifier = train_model()

#model = MODEL_API(classifier, X, y_true, sex)

@app.get("/get_size")
async def know_data_size():
    return len(X)

@app.post("/sample")
async def sample(idx: List[int]):

    X_ = X.iloc[idx] #shd be a valid pd frame
    y_ = y_true.iloc[idx] #pd series
    sensitive = sex.iloc[idx]
    # note: it is better to conver series to dataframe for more consistency
    return {"feature": X_.to_dict(), "label": y_.to_frame(name="label").to_dict(), "sensitive": sensitive.to_frame(name="sex").to_dict()} 

@app.post("/predict")
async def predict(X: dict):
        # predict or a pipeline, use sklearn convention
        X = pd.DataFrame(X)
        #return self.clf.predict(X)
        y_pred = classifier.predict(X)

        return pd.DataFrame(y_pred, columns=["predict"]).to_dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
    


    
