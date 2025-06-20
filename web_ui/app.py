# request is to access incoming form data/files
# redirect is to redirect the user to a different page
# url_for is to generate URLs for the application
# send_file is to send files to the user
# render_template is to render HTML templates for the web interface
from flask import Flask, request, redirect, url_for, send_file, render_template, send_from_directory

# os is for file system operations
# subprocess is to invoke our segmentation/font/render scripts
import os, subprocess

# Creates the Flask app
# __name__ tells Flask where to look for templates/static files
app = Flask(__name__)

# A place to stash uploads
UPLOAD_FOLDER = "uploads"

# Ensures the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok = True)

# "/" renders templeayes/index.html when someone visits the home pagae
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_template", methods = ["POST"])
def upload_template():
    # Grabs the uploaded file from the form field named "template"
    f = request.files("template")

    # Builds a safe path
    path = os.path.join(UPLOAD_FOLDER, "handwritten_template.jpg")

    # Saves the uploaded image to disk
    f.save(path)

    # Invokes our segmentation script to crop that image
    subprocess.run([
        "python3",
        "../segmentation/segment_glyphs.py",
    ], check = True, cwd = "segmentation")

    # Sends the user back to the home page after upload
    return redirect(url_for("index"))

@app.route("/build_font", methods = ["POST"])
def upload_transcript():
    # Grabs the uplaaded file from the form field named "transcript"
    f = request.files("transcript")

    # Builds a safe path
    path = os.path.join(UPLOAD_FOLDER, "transcript.txt")

    # Saves the uploaded transcript to disk
    f.save(path)

    # Invokes our font building and rendering script
    # TODO: build_font.py then render handwritten_notes.py

    # Returns the generated pdf
    return send_file("TODO_OUTPUT_PATH")

@app.route("/glyph_images/<filename>")
def glyph_image(filename):
    # Sends the requested glyph image from the glyph_images directory
    return send_from_directory("segmentation/glyph_images", filename)

@app.route("/preview")
def show_preview():
    # List all the generated glyph PNGs
    files = sorted(os.listdir("segmentation/glyph_images"))
    return render_template("preview.html", files = files)
