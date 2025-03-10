from flask import Flask, request, jsonify
from utils.GoogleSpreadSheetUpdate import update_google_spread_sheet

app = Flask(__name__)


@app.route('/api/cv-process', methods = ['POST'])
def cv_process() :

    try :
        applicant_name = request.form.get('applicant-name')
        applicant_email = request.form.get('applicant-email')
        apllicant_contact = request.form.get('applicant-contact')
        applicant_education = request.form.get('applicant-education')
        applicant_qualification = request.form.get('applicant-qualification')
        applicant_projects = request.form.get('applicant-projects')

        # update details in google spreadsheet
        try :
            google_sheet_data_update_status = update_google_spread_sheet(applicant_name, applicant_email, apllicant_contact, applicant_education, applicant_qualification, applicant_qualification)

            if google_sheet_data_update_status == False :
                return jsonify({
                    'message' : 'Something went wrong in data insertion process'
                })
                
        except Exception as e :
            print(f"Something went wrong in google sheet data insersion {str(e)}")
        
        return jsonify({
            'message' : 'success message'
        })

    except Exception as e :
        print(f"something went wrong {str(e)}")
        return jsonify({
            'message' : 'went wrong'
        })
    

if __name__ == "__main__" :
    app.run(debug=True, port=8080)