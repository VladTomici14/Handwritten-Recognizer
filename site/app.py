from flask import Flask, render_template, request, jsonify, session
import os
import warnings
import utils
from scanner import Scanner
from werkzeug.exceptions import HTTPException


def allowed_file(filename):
    file_extension = filename.split(".")[-1] in ("jpg", "jpeg", "png", "webp", "mp4", "mov", "avi")

    if not file_extension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")

warnings.filterwarnings("ignore")

app = Flask(__name__, template_folder="templates", static_folder="static")

# Set Environment Variables
UPLOAD_FOLDER = os.path.join("static/uploads")
OUTPUT_FOLDER = os.path.join("static/outputs")
# The config is actually a subclass of a dictionary and can be modified just like any dictionary

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "xyz"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/"
os.path.dirname("templates")

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/', methods=["POST"])
def uploadFile():
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):  # Create Directory for the uploaded static
        os.mkdir(app.config["UPLOAD_FOLDER"])

    _img = request.files["file-uploaded"]
    filename = _img.filename
    allowed_file(filename)
    _img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    session["uploaded_img_file_path"] = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    return render_template("index.html", success=True)


@app.route("/show_file")
def displayImage():
    img_file_path = session.get("uploaded_img_file_path", None)

    return render_template("show_file.html", user_image=img_file_path, is_image=True, is_show_button=True)

    # if img_file_path.split(".")[-1] in ("mp4", "mov"):
    #     return render_template("show_file.html", user_image=img_file_path, is_image=False, is_show_button=True)
    # else:
    #     return render_template("show_file.html", user_image=img_file_path, is_image=True, is_show_button=True)


@app.route("/detect_object")
def detectObject():
    uploaded_image_path = session.get("uploaded_img_file_path", None)
    # output_image_path, response, file_type = detect_and_draw_box(uploaded_image_path)

    scanner = Scanner()
    output_image_path = scanner.returnScan(uploaded_image_path)
    
    return render_template("show_file.html", user_image=output_image_path, is_image=True, is_show_button=False)

    # if file_type == "image":
    #     return render_template("show_file.html", user_image=output_image_path, is_image=True, is_show_button=False)
    # else:
    #     return render_template("show_file.html", user_image=output_image_path, is_image=False, is_show_button=False)


# @app.route('/get-items')
#
# def get_items():
#     return jsonify(aws_controller.get_items())

if __name__ == "__main__":
    app.run(debug=True)
