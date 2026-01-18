const fileInput = document.getElementById("file");
const uploadBtn = document.getElementById("upload-btn");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        document.getElementById("file-name").textContent =
            fileInput.files[0].name;
        uploadBtn.disabled = false;
    }
});

function upload() {
    const file = fileInput.files[0];
    if (!file) return;

    uploadBtn.disabled = true;
    document.getElementById("status").textContent = "";

    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            document.getElementById("progress-container").style.display = "block";
            document.getElementById("progress-bar").style.width = percent + "%";
            document.getElementById("progress-text").textContent = percent + "%";
        }
    };

    xhr.onload = () => {
        document.getElementById("status").textContent = xhr.responseText;
    };

    xhr.onerror = () => {
        document.getElementById("status").textContent = "Upload failed";
    };

    xhr.send(formData);
}