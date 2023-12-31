import logging
import os
from flask import Flask, request, jsonify, render_template, send_file
from scripts.totaljobs import Bot
from loguru import logger

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class WerkzeugHandler(logging.Handler):
    def emit(self, record):
        loguru_logger = logger.bind(request_id=record.request.environ.get('FLASK_REQUEST_ID', 'unknown'))
        loguru_logger.opt(depth=6, exception=record.exc_info).log(record.levelname, record.getMessage())


app.logger.handlers = [WerkzeugHandler()]  # adds handler to the werkzeug WSGI logger

logger.add("server.log", rotation="500 MB", level="INFO")


@app.route('/image/<image_name>')
def serve_image(image_name):
    # Build the path to the image file
    image_path = f'static/images/{image_name}'  # Assuming the images are in the 'static' folder

    # Use send_file to send the image to the client
    return send_file(image_path, as_attachment=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/apply', methods=['POST'])
def run_playwright():
    logger.info('Received a request', extra=request.data)
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
