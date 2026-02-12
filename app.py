from flask import Flask, render_template, request, jsonify
from utils.text_extractor import extract_text
from utils.matcher import match_resume

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    resume_file = request.files['resume']
    job_description = request.form['job_description']

    resume_text = extract_text(resume_file)

    result = match_resume(resume_text, job_description)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
