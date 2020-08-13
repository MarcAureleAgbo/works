import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb')) #Import du modèle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST']) #page predict crée et grace a la methode POST, on peut l'ouvrir
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()] #valeurs i
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='La réponse à votre requête {}'.format(output))



if __name__ == "__main__":
    app.run(debug=True)