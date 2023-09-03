import os
from flask import Flask, request, jsonify
from scripts.totaljobs import Bot

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/apply', methods=['POST'])
def run_playwright():
    check_resume()
    try:

        bot = Bot(job_type=request.form['desiredJobType'], minimum_salary=int(request.form['minimumSalary']),
                  required_skills=list(request.form['skills']),
                  match_threshold=int(request.form['skillMatchThreshold']),
                  date_posted=int(request.form['jobsLessThan']), email=str(request.form['email']),
                  first_name=str(request.form['first_name']), surname=str(request.form['surname']),
                  password=str(request.form['password']))
        bot.setup_browser()
        bot.search_for_job(job_title=request.form['jobTitle'], location=request.form['location'])

        result = "Script executed successfully"
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e))


def check_resume():
    if 'cv' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    cv_file = request.files['cv']
    # Check if the file is a PDF
    if cv_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not cv_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Uploaded file is not a PDF'}), 400
    # Save the PDF file to the server
    if cv_file:
        cv_filename = os.path.join(app.config['UPLOAD_FOLDER'], cv_file.filename)
        cv_file.save(cv_filename)


if __name__ == '__main__':
    app.run(debug=True)
