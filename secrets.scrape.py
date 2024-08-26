import argparse
import os
import shutil
import zipfile
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def download_view_source_html(view_source_url):
    # Remove 'view-source:' prefix
    url = view_source_url.replace('view-source:', '')

    response = requests.get(url, stream=True)
    if not response.status_code == 200:
        return None

    filename = f"{urlparse(url).netloc}_Source.html"
    with open(filename, 'wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=8192), desc="Downloading Source HTML"):
            if chunk:
                file.write(chunk)

    print(f"Downloaded Source HTML to {filename}")
    return filename


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
            # Correctly concatenate the base URL and the relative URL
            img_url = f"{base_url}/{img_url}"
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


def parse():
    parser = argparse.ArgumentParser(description='Web Scraper - Ultra -> Includes SECRETS Scraping')
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

    def download(url, non=False):
        if args.full:
            filename = download_with_resources(url)
            images = download_images(url, url)

            # Create a folder to store all files
            folder_path = f"{website_name}_{args.full and 'full' or 'basic'}_files"
            os.makedirs(folder_path, exist_ok=True)

            # Save the HTML file
            if filename:
                shutil.copy(filename, folder_path)

            # Download and save images
            if images:
                for image in images:
                    image_path = os.path.join(folder_path, os.path.basename(image))
                    img_response = requests.get(image, stream=True)
                    with open(image_path, 'wb') as img_file:
                        for chunk in tqdm(img_response.iter_content(chunk_size=8192),
                                          desc=f"Downloading Image {os.path.basename(image)}"):
                            if chunk:
                                img_file.write(chunk)
        else:
            filename = download_basic_html(url)
            folder_path = f"{website_name}_basic_files"
            os.makedirs(folder_path, exist_ok=True)
            shutil.copy(filename, folder_path)

        # Zip the contents of the folder
        if args.zip:
            zip_filename = f"{website_name}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file),
                                                   os.path.join(folder_path, '..')))
            print(f"Files zipped into {zip_filename}")

            # Optionally, delete the folder after zipping
            shutil.rmtree(folder_path)
            print(f"Folder {folder_path} deleted.")
        else:
            print(f"All files saved in {folder_path}")

        if non:
            ext = ".txt"
        else:
            ext = ".html"

        try:
            os.remove(website_name + "_basic" + ext)
            print(f"File {website_name + '_basic' + ext} deleted.")
        except Exception:
            try:
                os.remove(website_name + "_advanced" + ext)
                print(f"File {website_name + '_basic_files' + ext} deleted.")
            except Exception as e:
                print("Error deleting files:", e)

    download(args.url)

    download(args.url + "/robots.txt", True)

    download_view_source_html("view-source:" + args.url)


if __name__ == "__main__":
    parse()
