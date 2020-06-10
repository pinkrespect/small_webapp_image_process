import subprocess
import sys
from subprocess import Popen, PIPE, check_output
from flask import Flask, Response, request, redirect, url_for, render_template, session, app
import os

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import hashlib
import time


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SCT_YEK_ER'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploaded_images') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



def uploaded():
    def inner():
        proc = subprocess.Popen('./some.sh', stderr=PIPE, stdout=PIPE, shell=True, executable="/bin/bash")
        for line in iter(proc.stdout.readline,b''):
            print(line)
            string = line.rstrip()
            if line == b'Success\n':
                string = b'<a href="./show_image"> Click Here </a><br/>\n' 
            yield string + b'<br/>\n'

        for line in iter(proc.stderr.readline,b''):
            string = line.rstrip()
            yield string + b'<br/>\n'
    return Response(inner(), mimetype='text/html')


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')


@app.route('/', methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = request.files.getlist('photo')
        name = str("image") 
        print(filename)
        photos.save(filename[0], name=name + '.')
        name = str("stylized") 
        photos.save(filename[1], name=name + '.')
        success = True
        return redirect(url_for('running_process'))
    else:
        success = False
    return render_template('index.html', form=form, success=success)


@app.route('/upload_complete', methods=["POST", "GET"])
def running_process():
    return uploaded()

@app.route('/show_image', methods=["GET", "POST"])
def show_result():
    image_file = url_for('static', filename="output/output.png")
    return render_template('image_complete.html', image_file=image_file)


@app.teardown_request
def job_done(exception):
    return exception


if __name__ == '__main__':
    app.config['SERVER_NAME'] = "0.0.0.0:9000"
    app.run(debug=True, host='0.0.0.0', port=9000)

