function generatePost() {
    let url = document.getElementById("movieUrl").value;
    if (!url) {
        alert("Please enter a movie URL!");
        return;
    }
    fetch('/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movieUrl: url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").value = data.html;
    })
    .catch(error => console.error("Error:", error));
}

function copyToClipboard() {
    let output = document.getElementById("output");
    output.select();
    document.execCommand("copy");
    alert("Copied to clipboard!");
}
