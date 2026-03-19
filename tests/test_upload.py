import io
import os
import pytest
from upload_server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_upload_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_file_upload(client):
    data = {
        "file": (io.BytesIO(b"hello world"), "test.txt")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert b"Uploaded: test.txt" in response.data

    file_path = os.path.join(app.config['UPLOAD_DIR'], "test.txt")

    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        content = f.read()

    assert content == b"hello world"


def test_path_traversal_upload(client):
    data = {
        "file": (io.BytesIO(b"malicious content"), "../malicious.txt")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert b"Uploaded: malicious.txt" in response.data  # File is saved safely as malicious.txt

    file_path = os.path.join(app.config['UPLOAD_DIR'], "malicious.txt")

    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        content = f.read()

    assert content == b"malicious content"
