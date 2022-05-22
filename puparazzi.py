# pup-arazzi.py

from bentoml.frameworks.fastai import Fastai1ModelArtifact
from bentoml.adapters import FileInput
from fastcore.utils import tuplify, detuplify

import bentoml

# Define the model artifact for prediction
@bentoml.artifacts([Fastai1ModelArtifact('learner')])

# Define the environment. Infer pip package requirements.
@bentoml.env(infer_pip_packages=True)

# Define the service that handles the model
class PuparazziService(bentoml.BentoService):

    # Define the api
    @bentoml.api(input=FileInput(), batch=False)
    def predict(self, file):
        files = [i.read() for i in files]
        dl = self.artifacts.learner.dls.test_dl([file.read()], rm_type_tfms=None, num_workers=0)
        inp, preds, _, dec_preds = self.artifacts.learner.get_preds(dl=dl, with_input=True, with_decoded=True)
        i = getattr(self.artifacts.learner.dls, 'n_inp', 1)
        inp = (inp,)
        dec_list = self.artifacts.learner.dls.decode_batch(inp + tuplify(dec_preds))
        res = []
        for dec in dec_list:
            dec_inp, dec_targ = map(detuplify, [dec[:i],dec[i:]])
            res.append(dec_targ)
        return res