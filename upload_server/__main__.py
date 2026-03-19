#!/usr/bin/env python
"""
Filename    : __main__.py
Porject     : Upload Server
Description : Uplaod server to receive file from network via HTTP.
"""

# standard import
import os
import argparse

# third party imports
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Default configurations, can be overridden by CLI args or tests
app.config['UPLOAD_DIR'] = "uploads"
app.config['CUSTOM_MESSAGE'] = "Send a file to Viktor Mac"

@app.before_request
def setup_upload_dir():
    """Ensure the upload directory exists before each request"""
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    """Defining route to upload files"""
    if request.method == "POST":
        files = request.files.getlist("file")
        uploaded_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_DIR'], filename)
                file.save(path)
                uploaded_files.append(filename)
        if uploaded_files:
            return ""
    return render_template("upload.html", message=app.config['CUSTOM_MESSAGE'])

def parse_args():
    """Parse runtime arguments"""
    parser = argparse.ArgumentParser(
        description="Upload server to receive files from network via HTTP.")
    parser.add_argument("--port", type=int, default=8000,
                    help="Port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0",  # nosec B104
                    help="Address to listen on (default: 0.0.0.0)")
    parser.add_argument("--upload-dir", type=str, default="uploads",
                    help="Directory to save uploaded files (default: uploads)")
    parser.add_argument("--message", type=str,
                    default="Send a file to Viktor Mac",
                    help="Custom message to display on the upload page")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    app.config['UPLOAD_DIR'] = args.upload_dir
    app.config['CUSTOM_MESSAGE'] = args.message
    app.run(host=args.host, port=args.port)
