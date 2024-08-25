import requests
from urllib.parse import urlparse
import sys


def check_robots(URL):
    robots_url = f"{URL}/robots.txt"
    response = requests.get(robots_url)
    return response.status_code == 200


def read_robots_txt(URL):
    robots_url = f"{URL}/robots.txt"
    response = requests.get(robots_url)
    return response.text


def scrape_directories(URL):
    if not check_robots(URL):
        print("robots.txt not found")
        return

    robots_content = read_robots_txt(URL)

    parsed_url = urlparse(URL)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    with open('directories.txt', 'w') as f:
        for line in robots_content.splitlines():
            if line.startswith('Disallow'):
                directory = line.split(':')[1].strip()
                scraped_url = f"{base_url}/{directory}"
                try:
                    requests.get(scraped_url)
                    f.write(f"Scraped {scraped_url}\n")
                except Exception as e:
                    print(f"Error scraping {scraped_url}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Checking {url}")
    check_robots(url)
    scrape_directories(url)
