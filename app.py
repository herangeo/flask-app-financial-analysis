from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from model import probe_model_5l_profit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data.json')
        file.save(filepath)

        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
        
        # Run the financial analysis model
        result = probe_model_5l_profit(data['data'])

        # Pass result to results page
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run()
