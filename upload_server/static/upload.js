const fileInput = document.getElementById("file");
const uploadBtn = document.getElementById("upload-btn");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        if (fileInput.files.length === 1) {
            document.getElementById("file-name").textContent = fileInput.files[0].name;
        } else {
            document.getElementById("file-name").textContent = fileInput.files.length + " files selected";
        }
        uploadBtn.disabled = false;
    } else {
        document.getElementById("file-name").textContent = "No file selected";
        uploadBtn.disabled = true;
    }
});

function upload() {
    if (fileInput.files.length === 0) return;

    uploadBtn.disabled = true;
    document.getElementById("status").textContent = "";

    const fileList = document.getElementById("file-list");
    fileList.innerHTML = ""; // Clear out previous items

    const globalContainer = document.getElementById("progress-container");
    const globalBar = document.getElementById("progress-bar");
    const globalText = document.getElementById("progress-text");
    globalContainer.style.display = "block";
    globalBar.style.width = "0%";
    globalText.textContent = "0%";

    const totalBytes = Array.from(fileInput.files).reduce((acc, file) => acc + file.size, 0);
    const loadedBytesPerFile = new Array(fileInput.files.length).fill(0);

    function updateGlobalProgress() {
        if (totalBytes === 0) return;
        const totalLoaded = loadedBytesPerFile.reduce((acc, current) => acc + current, 0);
        const percent = Math.round((totalLoaded / totalBytes) * 100);
        globalBar.style.width = percent + "%";
        globalText.textContent = percent + "%";
    }

    for (let i = 0; i < fileInput.files.length; i++) {
        const file = fileInput.files[i];

        const itemDiv = document.createElement("div");
        itemDiv.className = "file-item";

        const headerDiv = document.createElement("div");
        headerDiv.className = "file-header";

        const nameSpan = document.createElement("span");
        nameSpan.className = "file-name-text";
        nameSpan.textContent = file.name;

        const iconSpan = document.createElement("span");
        iconSpan.className = "file-status-icon";
        iconSpan.textContent = "0%";

        headerDiv.appendChild(nameSpan);
        headerDiv.appendChild(iconSpan);

        const progressBg = document.createElement("div");
        progressBg.className = "progress-bar-bg";

        const progressBar = document.createElement("div");
        progressBar.className = "progress-bar";
        progressBar.style.width = "0%";

        progressBg.appendChild(progressBar);

        itemDiv.appendChild(headerDiv);
        itemDiv.appendChild(progressBg);
        fileList.appendChild(itemDiv);

        const formData = new FormData();
        formData.append("file", file);

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/", true);

        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                loadedBytesPerFile[i] = e.loaded;
                updateGlobalProgress();

                const percent = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percent + "%";
                iconSpan.textContent = percent + "%";
            }
        };

        xhr.onload = () => {
            if (xhr.status === 200) {
                loadedBytesPerFile[i] = file.size; // Cap off the file load
                updateGlobalProgress();
                iconSpan.textContent = "✓";
                iconSpan.classList.add("success");
            } else {
                iconSpan.textContent = "Failed";
                iconSpan.style.color = "red";
            }
        };

        xhr.onerror = () => {
            iconSpan.textContent = "Error";
            iconSpan.style.color = "red";
        };

        xhr.send(formData);
    }
}