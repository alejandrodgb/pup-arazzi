# Import required libraries and services
from fastai.vision.all import *
from puparazzi import PuparazziService

# Create a service instance
svc = PuparazziService()

# Save path for deployment
spath = Path(f'{os.environ["HOME"]}/bentoml/repository/{svc.name}/')

# Load learner
lpath = os.path.dirname(os.path.abspath(__file__))
learner = load_learner(f'{lpath}/models/pup-arrazi_resnet101.pkl', cpu=True)
# Update path from the one saved when creating the model
learner.path = spath

# Pack the trained model artifact
svc.pack('learner', learner)

# Save to directory
svc.save()

# Move learner to package version
shutil.move(f'{spath}/learner.pkl', f'{spath}/{svc.version}/{svc.name}')