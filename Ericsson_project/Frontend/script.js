Dropzone.options.myDropzone = {
    url: "http://127.0.0.1:5000/upload",  // Updated to match backend URL
    method: "post",
    acceptedFiles: ".txt",
    maxFilesize: 5, // MB
    timeout: 180000, // Set timeout to 3 minutes
    init: function() {
        this.on("addedfile", function(file) {
            console.log("File added:", file.name);
        });
        this.on("sending", function(file, xhr, formData) {
            console.log("Sending file:", file.name);
        });
        this.on("success", function(file, response) {
            console.log("File uploaded successfully:", response);
            showUploadStatus(true);
        });
        this.on("error", function(file, errorMessage, xhr) {
            console.error("Error uploading file:", errorMessage);
            if (xhr) {
                console.error("Status:", xhr.status);
                console.error("Response:", xhr.responseText);
            }
            showUploadStatus(false, errorMessage);
        });
    }
};

// Test server connectivity
fetch("http://127.0.0.1:5000/upload", {method: "OPTIONS"})
    .then(response => console.log("Server is reachable"))
    .catch(error => console.error("Cannot reach server:", error));
function showUploadStatus(success, message) {
    const statusElement = document.getElementById('upload-status');
    statusElement.classList.remove('hidden');
    statusElement.classList.add('show');
    
    if (success) {
        statusElement.innerHTML = '<i class="fas fa-check-circle"></i> <span>Upload successful!</span>';
        statusElement.style.backgroundColor = 'rgba(46, 204, 113, 0.8)';
    } else {
        statusElement.innerHTML = `<i class="fas fa-times-circle"></i> <span>Upload failed: ${message}</span>`;
        statusElement.style.backgroundColor = 'rgba(231, 76, 60, 0.8)';
    }

    setTimeout(() => {
        statusElement.classList.remove('show');
        setTimeout(() => {
            statusElement.classList.add('hidden');
        }, 300);
    }, 5000);
}

// Test server connectivity
fetch("http://localhost:5000/upload", {method: "OPTIONS"})
    .then(response => console.log("Server is reachable"))
    .catch(error => console.error("Cannot reach server:", error));