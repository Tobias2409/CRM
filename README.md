# CRM

## Prerequisites
To run this Project you need an PC running Windows (Tested: Windows 11) with Python 3 installed.

## Installation
1) Clone this Repository
2) Execute the setup.bat which will install all python libaries
3) Change Import in keras_vggface (https://stackoverflow.com/questions/51337558/how-to-import-keras-engine-topology-in-tensorflow) 
Execute "pip show keras_vggface" to show libary location
In "keras_vggface/models.py" \
change \
from keras.engine.topology import get_source_inputs \
to \
from keras.utils.layer_utils import get_source_inputs

## PIP Installs

pip install opencv-python \
pip install face_recognition \
pip install mtcnn \
pip install tensorflow \
pip install keras \
pip install keras_vggface \
pip install keras_applications \
pip install icrawler 


## Usage
After Installing all Libaries, simply execute the start.bat
