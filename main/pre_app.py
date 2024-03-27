from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
# importing model
import joblib

joblib.load('crop_app', 'r')
model = joblib.load(open('crop_app', 'rb'))


# creating flask app
pre_app = Flask(__name__, template_folder='templates')

@pre_app.route('/')
def index():
    return render_template("index.html")

@pre_app.route("/predict", methods=['POST'])
def predict():
    try:
        Nitrogen = float(request.form['Nitrogen'])
        Phosphorus = float(request.form['Phosphorus'])
        Potassium = float(request.form['Potassium'])
        Temperature = float(request.form['Temperature'])
        Humidity = float(request.form['Humidity'])
        pH = float(request.form['pH'])
        Rainfall = float(request.form['Rainfall'])

        values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall]

        if 0 < pH <= 14 and 0 < Temperature < 100 and 0 < Humidity:
            arr = np.array(values).reshape(1,-1)
            acc = model.predict(arr)
            return render_template('index.html', result='Recommend Crop for cultivation is' + " "+str(acc[0]))
        else:
            return  render_template('index.html', result="Sorry... Error in entered values in the form. Please check the values and fill it again")
    except Exception as e:
        return "An error occurred: " + str(e)

# python main
if __name__ == "__main__":
    pre_app.run(debug=True)