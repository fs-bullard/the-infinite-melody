# import os
from flask import Flask, render_template, redirect

# import torch
# import numpy as np
# import torch.nn as nn
# import random
# from torch.autograd import Variable
# from os.path import join
# import __main__

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"

@app.route('/')
def root():
    return render_template('index.html')

@app.route("/soundcloud", methods=["GET"])
def to_soundcloud():
    return redirect("https://soundcloud.com/ben-welch-203938063/sets/the-infinite-melody?si=0166bd2f880b4e0fb3ab0bd51f1d609b&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing", code=302)

@app.route("/github", methods=["GET"])
def to_github():
    return redirect("https://github.com/fs-bullard/the-infinite-melody", code=302)

@app.route("/devpost", methods=["GET"])
def to_devpost():
    return redirect("https://devpost.com/software/the-infinite-melody", code=302)

if __name__ == '__main__':
    app.run(debug=True)