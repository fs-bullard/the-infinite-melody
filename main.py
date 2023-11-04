import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('page.html', title='The Infinite Melody')
    
if __name__ == '__main__':
    app.run(debug=True)