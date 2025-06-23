# web_ui/app.py

# request is to access incoming form data/files
# redirect is to redirect the user to a different page
# url_for is to generate URLs for the application
# send_file is to send files to the user
# render_template is to render HTML templates for the web interface
# send_from_directory is serve individual PNG glyphs
from flask import Flask, request, redirect, url_for, send_file, render_template, send_from_directory

# os is for file system operations
# subprocess is to invoke our segmentation/font/render scripts
# shutil is to copy files
import os, subprocess, shutil

# Creates the Flask app
# __name__ tells Flask where to look for templates/static files
app = Flask(__name__)

# A place to stash uploads
UPLOAD_FOLDER = "uploads"

# Ensures the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok = True)

# Computes project root so we can call scripts outside of web_ui/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# "/" renders templeayes/index.html when someone visits the home pagae
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_template", methods = ["POST"])
def upload_template():
    # Grabs the uploaded file from the form field named "template"
    f = request.files["template"]

    # Saves it under the uploads directory
    template_path = os.path.join(UPLOAD_FOLDER, "handwritten_template.jpg")

    # Saves the uploaded image to disk
    f.save(template_path)

    # Copies the uploaded template to the segmentation directory
    seg_input = os.path.join(PROJECT_ROOT, "segmentation", "handwritten_template.jpg")
    shutil.copy(template_path, seg_input)

    # Invokes our segmentation script to crop that image
    subprocess.run(
        ["python3", "../segmentation/segment_glyphs.py"],
        cwd = os.path.join(PROJECT_ROOT, "segmentation"),
        check = True
    )

    # Sends the user back to the home page after upload
    return redirect(url_for("show_preview"))

@app.route("/upload_transcript", methods = ["POST"])
def upload_transcript():
    # Grabs the uploaded file from the form field named "transcript"
    if "transcript" not in request.files or not request.files["transcript"].filename:
        return "No transcript file provided in the request.", 400

    f = request.files["transcript"]

    # Builds a safe path
    transcript_path = os.path.join(UPLOAD_FOLDER, "transcript.txt")

    # Saves the uploaded transcript to disk
    f.save(transcript_path)

    # Builds the font
    subprocess.run(
        ["fontforge", "-script", os.path.join(PROJECT_ROOT, "font_build", "build_font.py")],
        check = True
    )

    # Grabs the generated PDF
    output_pdf = os.path.join(PROJECT_ROOT, "rendering", "output", "notes.pdf")
    os.makedirs(os.path.dirname(output_pdf), exist_ok = True)

    # Renders the notes
    subprocess.run(
        [
            "python3",
            os.path.join(PROJECT_ROOT, "rendering", "render_handwritten_notes.py"),
            transcript_path,
            "--output",
            output_pdf
        ],
        check = True
    )

    # Returns the generated pdf
    return send_file(output_pdf, as_attachment = True)

@app.route("/glyph_images/<filename>")
def glyph_image(filename):
    glyph_dir = os.path.join(PROJECT_ROOT, "segmentation", "glyph_images")
    # Sends the requested glyph image from the glyph_images directory
    return send_from_directory(glyph_dir, filename)

@app.route("/preview")
def show_preview():
    glyph_dir = os.path.join(PROJECT_ROOT, "segmentation", "glyph_images")

    # List all the generated glyph PNGs
    files = sorted(os.listdir(glyph_dir))
    return render_template("preview.html", files = files)

if __name__ == "__main__":
    # 'python app.py' will start the dev server
    app.run(debug = True)