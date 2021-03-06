import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, flash, make_response, jsonify
from werkzeug.utils import secure_filename

from shubh_predict import predict

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'path\\uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    ans = 'shubbhang'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            ans = predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("--",ans,"--")

            # response = make_response(
            #     jsonify(
            #         {"message": ans, "severity": "danger"}
            #     )
            # )
            message = ans

            

            return redirect(url_for('uploaded_file', filename = filename, ans = ans))
            
            # return redirect(url_for('uploaded_file',filename=filename))
    print(">> ", ans, "<<<")
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # ''' 
    return render_template('upload.html')

@app.route('/uploads/<filename>/<ans>')
def uploaded_file(filename, ans):

    return make_response(send_from_directory(app.config['UPLOAD_FOLDER'],filename),ans)
    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == '__main__':
   app.run(debug = True)