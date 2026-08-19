import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_images(folder_name, query, limit):
    # Create a directory to store images
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Perform a Google search for images
    image_urls = []
    num_results_per_page = 10  # Number of results per page
    pages_needed = (limit + num_results_per_page - 1) // num_results_per_page  # Calculate number of pages needed
    for page in range(pages_needed):
        start_index = page * num_results_per_page
        search_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote_plus(query)}&start={start_index}"
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith("http"):  # Only valid URLs
                image_urls.append(src)
        if len(image_urls) >= limit:
            break

    # Download images
    for i, url in enumerate(image_urls[:limit]):
        try:
            img_data = requests.get(url).content
            with open(f"{folder_name}/{i+1}.jpg", 'wb') as handler:
                handler.write(img_data)
            print(f"Image {i+1} downloaded successfully")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")

if __name__ == "__main__":
    folder_name = input("Enter the folder name to save images: ").strip()
    query = input("Enter what images to download from Google: ").strip()
    limit = int(input("Enter the number of images to download: ").strip())

    download_images(folder_name, query, limit)
