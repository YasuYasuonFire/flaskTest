from flask import Flask
import io
import os
import warnings

from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

app = Flask(__name__)

@app.route("/")
def hello_world():
   return "<p>Hello, World!</p>"


@app.route('/hello/<name>')
def hello(name):
    return name