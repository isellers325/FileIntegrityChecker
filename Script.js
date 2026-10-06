const resultsDiv = document.getElementById("results");
const buildBtn = document.getElementById("buildBtn");
const checkBtn = document.getElementById("checkBtn");

buildBtn.addEventListener("click", function() {
    fetch("http://127.0.0.1:5000/api/build", { method: "POST" })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        resultsDiv.innerHTML = `<p class="ok">Baseline set: ${data.files_hashed} file(s) hashed.</p>`;
    });
});

checkBtn.addEventListener("click", function() {
    fetch("http://127.0.0.1:5000/api/check")
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        resultsDiv.innerHTML = "";

        if (data.modified.length === 0 && data.missing.length === 0 && data.new.length === 0) {
            resultsDiv.innerHTML = `<p class="ok">No changes detected.</p>`;
            return;
        }

        data.modified.forEach(function(filename) {
            resultsDiv.innerHTML += `<p class="failed">Modified: ${filename}</p>`;
        });
        data.missing.forEach(function(filename) {
            resultsDiv.innerHTML += `<p class="failed">Missing: ${filename}</p>`;
        });
        data.new.forEach(function(filename) {
            resultsDiv.innerHTML += `<p class="failed">New: ${filename}</p>`;
        });
    });
});
