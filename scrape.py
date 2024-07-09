import argparse
import os
import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urlparse
from tqdm import tqdm


def download_basic_html(url):
    response = requests.get(url, stream=True)  # Enable streaming for progress bar
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return None

    filename = f"{urlparse(url).netloc}_basic.html"
    with open(filename, 'wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=8192), desc="Downloading Basic HTML"):
            if chunk:
                file.write(chunk)

    print(f"Downloaded basic HTML to {filename}")
    return filename


def download_with_resources(url):
    response = requests.get(url, stream=True)  # Enable streaming for progress bar
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    resources = [link['href'] for link in soup.find_all('link', href=True)] + \
                [script.get('src', '') for script in soup.find_all('script', src=True)]

    print(f"Found resources: {resources}")  # In a real scenario, you'd download these resources

    filename = f"{urlparse(url).netloc}_advanced.html"
    with open(filename, 'wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=8192), desc="Downloading Advanced HTML"):
            if chunk:
                file.write(chunk)

    print(f"Downloaded advanced HTML to {filename}")
    return filename


def download_images(base_url, url):
    response = requests.get(url, stream=True)  # Enable streaming for progress bar
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    images = []
    for tag in image_tags:
        img_url = tag.get('src')
        if img_url and ('http' not in img_url and 'https' not in img_url):
            # Convert relative URL to absolute
            img_url = urlparse(base_url).scheme + '://' + urlparse(base_url).hostname + img_url
        images.append(img_url)

    print(f"Found images: {images}")  # In a real scenario, you'd download these images

    return images


def zip_files(zip_filename, files, delete_after=False):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to {zip_filename}")
            else:
                print(f"Warning: File {file} does not exist.")
    if delete_after:
        for file in files:
            os.remove(file)
            print(f"Deleted {file}")


def main():
    parser = argparse.ArgumentParser(description='Web Scraper')
    parser.add_argument('--name', default=None, help='Name of the website (optional)')
    parser.add_argument('--zip', action='store_true', help='Zip the downloaded files (default: False)')
    parser.add_argument('--full', action='store_true', help='Download full data or just basic UI (default: False)')
    parser.add_argument('--url', required=True, help='URL to scrape')
    parser.add_argument('-y', action='store_true', help='Automatically download without asking')

    args = parser.parse_args()

    website_name = args.name or urlparse(args.url).netloc
    print(f"Website Name: {website_name}")

    if not args.y:
        confirmation = input("Do you want to proceed? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Download cancelled.")
            return

    if args.full:
        filename = download_with_resources(args.url)
        images = download_images(args.url, args.url)

        if images:
            images_folder = f"{website_name}_images"
            os.makedirs(images_folder, exist_ok=True)
            for image in images:
                image_path = os.path.join(images_folder, os.path.basename(image))
                with open(image_path, 'wb') as img_file:
                    img_response = requests.get(image, stream=True)
                    for chunk in tqdm(img_response.iter_content(chunk_size=8192),
                                      desc=f"Downloading Image {os.path.basename(image)}"):
                        if chunk:
                            img_file.write(chunk)
    else:
        filename = download_basic_html(args.url)

    if args.zip and filename:
        zip_filename = f"{website_name}.zip"
        zip_files(zip_filename, [filename], delete_after=True)
        print(f"Files zipped into {zip_filename}")
    elif args.full:
        zip_filename = f"{website_name}_files.zip"
        zip_files(zip_filename, [filename] + images, delete_after=True)
        print(f"Files zipped into {zip_filename}")


if __name__ == "__main__":
    main()
