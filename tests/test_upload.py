import io
import os
import pytest
from upload_server import app, UPLOAD_DIR

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

    file_path = os.path.join(UPLOAD_DIR, "test.txt")

    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        content = f.read()

    assert content == b"hello world"
