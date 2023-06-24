import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
    """
    Make a prediction based on the input data and return the prediction
    """
    # Load the input data
    input_data = request.get_json(force=True)
    
    # Preprocess the input data
    input_data = np.array(input_data).reshape(-1, 1)
    
    # Load the trained model
    model = tf.keras.models.load_model("../models/trained_model.h5")
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0][0]})
