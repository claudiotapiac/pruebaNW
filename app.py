
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import torch
import torch.nn as nn
from model_atraso import AutoencoderClassifier
from flask_cors import CORS
from datetime import datetime, timezone, timedelta
import pandas as pd
import pytz
import os

app = Flask(__name__)
CORS(app)

model = AutoencoderClassifier(8)
model.load_state_dict(torch.load('./weight/model.pth')) 
model.eval()

def str_2_tensor(input_model):
  for i, value in enumerate(input_model):
    input_model[i] = float(value)
  input_model = torch.tensor(input_model, dtype=torch.float32)
  return input_model

@app.route('/',methods = ['POST', 'GET'])
def get():
  input_model = request.form.to_dict(flat=False)
  input_model = input_model['values']
  input_model = str_2_tensor(input_model)

  with torch.no_grad():
    output = model(input_model)
    print(output)
  result = {'value': output.item()}
  return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)


