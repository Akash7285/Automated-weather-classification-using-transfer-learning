import numpy as np
import os
from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.models import load_model

model_path = "E:\\Naanmudhalvan\\flask\\wcv.h5"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/input')
def input1():
    return render_template("input.html")

@app.route('/predict', methods=["POST"])
def res():
    if request.method == "POST":
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        upload_dir = os.path.join(basepath, 'uploads')

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        filepath = os.path.join(upload_dir, f.filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        img_data = preprocess_input(x)

        model = load_model(model_path)
        prediction = np.argmax(model.predict(img_data), axis=1)
        index = ['alien_test', 'cloudy', 'foggy', 'rainy', 'shine', 'sunrise']
        result = index[prediction[0]]

        return render_template('output.html', prediction=result)

if __name__ == '__main__':
    app.run()
