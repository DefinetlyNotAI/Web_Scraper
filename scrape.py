import argparse
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import zipfile
import os


def download_basic_html(url):
    """
    Downloads only the main HTML content of the website.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return None

    filename = f"{urlparse(url).netloc}_basic.html"
    with open(filename, 'wb') as file:
        file.write(response.content)

    print(f"Downloaded basic HTML to {filename}")
    return filename


def download_with_resources(url):
    """
    Attempts to download the main HTML content and lists resources like CSS and JS files.
    This is a simplified example and does not actually download the resources.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    resources = [link['href'] for link in soup.find_all('link')] + \
                [script['src'] for script in soup.find_all('script')]

    print(f"Found resources: {resources}")  # In a real scenario, you'd download these resources

    filename = f"{urlparse(url).netloc}_advanced.html"
    with open(filename, 'wb') as file:
        file.write(soup.prettify('utf-8'))

    print(f"Downloaded advanced HTML to {filename}")
    return filename


def zip_files(zip_filename, files):
    """
    Zips specified files into a single archive.
    """
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to {zip_filename}")
            else:
                print(f"Warning: File {file} does not exist.")


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
    else:
        filename = download_basic_html(args.url)

    if args.zip and filename:
        zip_filename = f"{website_name}.zip"
        zip_files(zip_filename, [filename])
        print(f"Files zipped into {zip_filename}")


if __name__ == "__main__":
    main()
