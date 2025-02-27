import requests
from bs4 import BeautifulSoup

def scrape_movie_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Unable to fetch the page"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No Title Found"
    
    # Extract description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else "No Description Found"
    
    # Extract all image URLs
    images = [img["src"] for img in soup.find_all("img") if "src" in img.attrs]
    
    # Format output
    output = f"""
    <h2>{title}</h2>
    <p>{description}</p>
    <h3>Screenshots:</h3>
    """
    
    for img_url in images[:6]:  # Limiting to 6 images as per requirement
        output += f'<img src="{img_url}" alt="Screenshot"><br>\n'
    
    return output

# Example usage
movie_url = "https://rogmovies.cfd/download-daaku-maharaaj-2025-hindi-dubbed-480p-720p-1080p/"
print(scrape_movie_page(movie_url))
