# pup-arazzi.py

from bentoml.frameworks.fastai import FastaiModelArtifact
from bentoml.adapters import FileInput
from fastcore.utils import tuplify, detuplify
from io import BytesIO
import json
import numpy as np

import bentoml

# Define the model artifact for prediction
@bentoml.artifacts([FastaiModelArtifact('learner')])

# Define the environment. Infer pip package requirements.
@bentoml.env(infer_pip_packages=True)

# Define the service that handles the model
class PuparazziService(bentoml.BentoService):

    # Define the api
    @bentoml.api(input=FileInput(), batch=False)
    def predict(self, file):
        # Read bytes 
        file = BytesIO(file.read())
        
        # Create dataloader
        dl = self.artifacts.learner.dls.test_dl([file.read()], rm_type_tfms=None, num_workers=0)
        
        # Get predictions
        inp, preds, _, dec_preds = self.artifacts.learner.get_preds(dl=dl, with_input=True, with_decoded=True)
        
        # Get classes
        classes = self.artifacts.learner.dls.vocab
        
        # Convert predictions to numpy objects
        predictions = np.array(preds.tolist()).reshape(-1)
        
        # Calculate the top 5 predictions, sort them
        k=5
        idxs = np.argpartition(predictions, -k)[-k:]
        probs = np.partition(predictions, -k)[-k:]
        cls = [classes[i] for i in idxs]
        topk = sorted([(p,c,i) for p,c,i in zip(probs,cls,idxs)],reverse=True)

        # Return a json object with probabilities, classes, and indexes in the classes list
        return json.dumps([{'prob':float(p),'class':c,'idx':int(i)} for p,c,i in topk])