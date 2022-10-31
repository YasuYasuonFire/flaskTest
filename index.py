from flask import Flask,send_file
from flask_cors import CORS

import io
import os
import warnings

from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
   return "<p>Hello, World!</p>"


@app.route('/hello/<name>')
def hello(name):
    return name

@app.route('/stableDiffusion/<text>')
def stable(text):
    # NB: host url is not prepended with \"https\" nor does it have a trailing slash.
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

    # To get your API key, visit https://beta.dreamstudio.ai/membership
    os.environ['STABILITY_KEY'] = "sk-X3VFeUijInA3cGmtq0tibEArVIF2hmPj0Dosn8nmjaYEk7aQ"

    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'], 
        verbose=True,
    )

    #debug
    print(text)

    # the object returned is a python generator
    answers = stability_api.generate(
        #prompt="houston, we are a 'go' for launch!",
        prompt=text,
        seed=34567, # if provided, specifying a random seed makes results deterministic
        steps=30, # defaults to 50 if not specified
    )
    
    # iterating over the generator produces the api response
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save('/tmp/output.jpg')
                return send_file('/tmp/output.jpg', mimetype='image/png')
