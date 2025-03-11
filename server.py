from flask import Flask, request, jsonify
from utils.GoogleSpreadSheetUpdate import update_google_spread_sheet
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import shutil

from data_embedding import load_extract_cv_data
from cv_data_extraction import process_cv
# from utils.utils import remove_cvs, cv_storing_process

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'cv-container'


# remove cvs in cv-container
def remove_cvs():
    cv_container_path = './cv-container'
    if os.path.exists(cv_container_path):
        try:
            shutil.rmtree(cv_container_path)
        except Exception as e:
            print(f"Something went wronf cv container clearing process.. {e}")
    else:
        print('path isnt exists')


# cv container and stote cv in container
def cv_storing_process(cv):
    cv_container_path = './cv-container'

    # check cv container is already exists or not
    if not os.path.exists(cv_container_path):
        os.mkdir(cv_container_path)
        
    # save file in the specific file directory
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(cv.filename))
    cv.save(file_path)

    return file_path



# route for handlinf proccessors of core
@app.route('/api/cv-process', methods = ['POST'])
def cv_process() :
    
    try:
        name = request.form.get('applicant_name')
        email = request.form.get('applicant_email')
        contact = request.form.get('applicant_contact')
        applicant_cv = request.files.get('pdf_file')

        # store cv in container
        file_path = cv_storing_process(applicant_cv)

        # extract and embeding cv data
        load_extract_cv_data(file_path)
        data = process_cv()
        
        # remove cvs from cv container
        remove_cvs()

        # update applicant details in google spreadsheet
        applicant_name = data.get('name')
        applicant_email = data.get('email')
        applicant_contact = data.get('contact')
        applicant_education = data.get('education')
        applicant_qualification = data.get('qualification')
        applicant_project = data.get('project')

        # store applicant details in google spreadsheet
        try :
            update_google_spread_sheet(applicant_name, applicant_email, applicant_contact, applicant_education, applicant_qualification, applicant_project)

            if update_google_spread_sheet:
                return jsonify({
                    'message' : 'Success'
                })
            else :
                return jsonify({
                    'message' : 'Something wrong'
                })
        except Exception as e:
            print(f"Something went wrong in data storing in spreadsheet... {e}")
        

    except Exception as e:
        print(f"Something went wrong in form handling.. {e}")
        return jsonify({
            'message' : 'Something wrnt wrong'
        })
    

if __name__ == "__main__" :
    app.run(debug=True, port=8080)