from flask import Flask, request, jsonify
from sklearn.externals import joblib
import numpy as np
from flask_cors import CORSss

app = Flask(__name__)
CORS(app)

clf = joblib.load('./model/logreg.pkl')

def getParameters():
