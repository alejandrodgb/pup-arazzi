# Import required libraries and services
from fastai.vision.all import *
from puparazzi import PuparazziService

# Load learner
learner = load_learner('models/pup-arrazi_resnet101.pkl')

# Create a service instance
svc = PuparazziService()

# Pack the trained model artifact
svc.pack('learner', learner)

# Save the model server to disk for model serving
saved_path = svc.save()