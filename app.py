from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_movie_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Unable to fetch the page"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting Title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No Title Found"

    # Extracting Description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else "No Description Found"

    # Extracting Screenshot URLs
    images = [img["src"] for img in soup.find_all("img") if "src" in img.attrs][:6]

    # Extracting Download Links
    download_links = []
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if "download" in href or "drive" in href:
            download_links.append(href)

    # Generating Blogger-compatible HTML
    html_output = f"""
    <h2>{title}</h2>
    <p><strong>Description:</strong> {description}</p>
    <h3>Screenshots:</h3>
    {"".join(f'<img src="{img}" width="300"><br>' for img in images)}
    <h3>Download Links:</h3>
    {"".join(f'<a href="{link}" target="_blank">Download</a><br>' for link in download_links)}
    """

    return {"html": html_output}

@app.route("/scrape", methods=["GET"])
def scrape():
    movie_url = request.args.get("url")
    if not movie_url:
        return jsonify({"error": "URL parameter is required"}), 400

    data = scrape_movie_page(movie_url)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
