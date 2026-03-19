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
        "file": [
            (io.BytesIO(b"hello world"), "test1.txt"),
            (io.BytesIO(b"second test"), "test2.txt")
        ]
    }

    response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200

    file_path1 = os.path.join(app.config['UPLOAD_DIR'], "test1.txt")
    file_path2 = os.path.join(app.config['UPLOAD_DIR'], "test2.txt")

    assert os.path.exists(file_path1)
    with open(file_path1, "rb") as f:
        content = f.read()
    assert content == b"hello world"

    assert os.path.exists(file_path2)
    with open(file_path2, "rb") as f:
        content = f.read()
    assert content == b"second test"


def test_path_traversal_upload(client):
    data = {
        "file": (io.BytesIO(b"malicious content"), "../malicious.txt")
    }

    response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200

    file_path = os.path.join(app.config['UPLOAD_DIR'], "malicious.txt")

    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        content = f.read()

    assert content == b"malicious content"
