from flask import Flask
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/gen')
def gen():

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content("The opposite of hot is")

    return response.text

@app.route('/about')
def about():
    return 'About'