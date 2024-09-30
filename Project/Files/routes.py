from flask import Blueprint, render_template, request, flash, redirect, current_app, send_file
from werkzeug.utils import secure_filename
from .models import Files
from . import db
import os

upload = Blueprint('upload', __name__)
download = Blueprint('download', __name__)

@upload.route("/", methods=["GET", "POST"])
def upload_file():
    UPLOAD_DIR = current_app.config['UPLOAD_FOLDER']
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
            new_file=Files(filename=filename, file_code="x")
            db.session.add(new_file)
            db.session.commit()
            print("Added")
            flash("File uploaded") 
    
    return render_template("home.html")

@upload.app_errorhandler(413)
def handle_413(error):
    flash("File is too large")
    return redirect(request.url), 413

@download.route("/", methods=["GET"])
def show_files():
    DOWNLOAD_DIR = current_app.config['UPLOAD_FOLDER']
    directory = os.listdir(DOWNLOAD_DIR)
    return render_template("downloads.html", directory=directory)

@download.route("/<filename>", methods=["GET"])
def download_files(filename):
    DOWNLOAD_DIR = current_app.config['UPLOAD_FOLDER']
    path = DOWNLOAD_DIR + "/" + filename
    return send_file(path, as_attachment=True)

