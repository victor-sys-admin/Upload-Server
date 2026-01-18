#!/usr/bin/env python
"""
Filename    : __main__.py
Porject     : Upload Server
Description : Uplaod server to receive file from network via HTTP.
"""

# standard import
import os

# third party imports
from flask import Flask, request, render_template

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    """Defining route to upload files"""
    if request.method == "POST":
        file = request.files["file"]
        if file.filename:
            path = os.path.join(UPLOAD_DIR, file.filename)
            file.save(path)
            return f"Uploaded: {file.filename}"
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) #nosec
