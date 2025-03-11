from flask import Flask, request, jsonify
from utils.GoogleSpreadSheetUpdate import update_google_spread_sheet
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'job_automation_secret'
app.config['UPLOAD_FOLDER'] = 'cv-container'

@app.route('/api/cv-process', methods = ['POST'])
def cv_process() :
    
    try:
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        applicant_contact = request.form.get('applicant_contact')
        applicant_cv = request.files.get('pdf_file')


        # save file in the specific file directory
        applicant_cv.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(applicant_cv.filename)))

        print(applicant_name,applicant_email, applicant_contact, applicant_cv)
        return jsonify({
            'message' : 'success'
        })
        
    except Exception as e:
        print(f"Something went wrong in form handling.. {e}")
        return jsonify({
            'message' : 'Something wrnt wrong'
        })
    

if __name__ == "__main__" :
    app.run(debug=True, port=8080)