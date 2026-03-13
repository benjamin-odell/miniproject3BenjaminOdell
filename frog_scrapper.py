import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

def getdata(url):
    r = requests.get(url)
    return r.text

def download_and_resize_image(img_url, output_dir="downloaded_frogs", size=(500, 500)):
    """Download an image from URL and resize it using Image.thumbnail()"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Download the image
        response = requests.get(img_url, timeout=5)
        response.raise_for_status()
        
        # Open image from bytes
        img = Image.open(BytesIO(response.content))
        
        # Resize using thumbnail (maintains aspect ratio)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Generate filename from URL
        filename = img_url.split('/')[-1].split('?')[0]
        if not filename:
            filename = f"frog_{hash(img_url) % 10000}.jpg"
        
        # Save the resized image
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)
        
        print(f"Downloaded and resized: {filename}")
        return output_path
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")
        return None

htmldata = getdata("https://enjoythewild.com/types-of-frogs/")
soup = BeautifulSoup(htmldata, 'html.parser')

# Download and resize all images
for item in soup.find_all('img'):
    img_url = item.get('src')
    if img_url:
        # Handle relative URLs
        if img_url.startswith('http'):
            download_and_resize_image(img_url)
        else:
            # If relative URL, you may need to construct full URL
            print(f"Skipping relative URL: {img_url}")
