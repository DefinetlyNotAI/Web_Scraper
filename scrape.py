import argparse
import os
import shutil
import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urlparse
from tqdm import tqdm


def download_basic_html(url):
    """
    Downloads the basic HTML content from a given URL and saves it to a file.

    Parameters:
        url (str): The URL of the HTML content to be downloaded.

    Returns:
        str or None: The filename of the downloaded HTML file, or None if the download failed.
    """
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
    """
    Downloads the HTML content and associated resources from a given URL, saves them to a file, and returns the filename.

    Parameters:
        url (str): The URL from which to download the HTML content and resources.

    Returns:
        str or None: The filename of the downloaded HTML file with associated resources, or None if the download failed.
    """
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
    """
    Downloads images from a given URL after processing them to get the absolute image URLs.

    Parameters:
        base_url (str): The base URL to be concatenated with relative image URLs.
        url (str): The URL from which to download the HTML content containing images.

    Returns:
        list: A list of absolute image URLs after concatenation with the base URL.
    """
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
    """
    Zips the files given in the 'files' list into a zip file named 'zip_filename'.

    Parameters:
        zip_filename (str): The name of the zip file to create.
        files (list): A list of file paths to be included in the zip.
        delete_after (bool, optional): Whether to delete the files after zipping. Defaults to False.
    """
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
    """
    Main function that serves as the entry point for the web scraping application.

    This function parses command line arguments to scrape a given URL, download content based on the arguments provided, and optionally zip the downloaded files.
    It prompts the user for confirmation before proceeding with the download.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Web Scraper')
    parser.add_argument('--name', default=None, help='Name of the website (optional)')
    parser.add_argument('--zip', action='store_true', help='Zip the downloaded files (default: False)')
    parser.add_argument('--full', action='store_true', help='Download full data or just basic UI (default: False)')
    parser.add_argument('--URL', required=True, help='URL to scrape')
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
        filename = download_basic_html(args.url)
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

    try:
        os.remove(website_name + "_basic.html")
        print(f"File {website_name + '_basic.html'} deleted.")
    except:
        try:
            os.remove(website_name + "_advanced.html")
            print(f"File {website_name + '_basic_files.html'} deleted.")
        except Exception as e:
            print("Error deleting files:", e)


if __name__ == "__main__":
    parse()
