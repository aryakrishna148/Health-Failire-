from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# load model
model = pickle.load(open("heart_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    features = np.array([[
        data["Age"],
        data["Sex"],
        data["ChestPainType"],
        data["RestingBP"],
        data["Cholesterol"],
        data["FastingBS"],
        data["RestingECG"],
        data["MaxHR"],
        data["ExerciseAngina"],
        data["Oldpeak"],
        data["ST_Slope"]
    ]])

    prediction = model.predict(features)

    return jsonify({"result": int(prediction[0])})


if __name__ == "__main__":
    app.run(debug=True)