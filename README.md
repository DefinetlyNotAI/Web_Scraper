# Web_Scraper 📎

Welcome to Web_Scraper 🌐,
a cutting-edge tool
designed to scrape webpages in a very neat fashion.
Crafted with python,

This comprehensive guide is here to equip you with everything you need
to use Web_Scraper effectively.

<div align="center">
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper/issues"><img src="https://img.shields.io/github/issues/DefinetlyNotAI/Web_Scraper" alt="GitHub Issues"></a>
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper/tags"><img src="https://img.shields.io/github/v/tag/DefinetlyNotAI/Web_Scraper" alt="GitHub Tag"></a>
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/t/DefinetlyNotAI/Web_Scraper" alt="GitHub Commit Activity"></a>
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper/languages"><img src="https://img.shields.io/github/languages/count/DefinetlyNotAI/Web_Scraper" alt="GitHub Language Count"></a>
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper/actions"><img src="https://img.shields.io/github/check-runs/DefinetlyNotAI/Web_Scraper/main" alt="GitHub Branch Check Runs"></a>
    <a href="https://github.com/DefinetlyNotAI/Web_Scraper"><img src="https://img.shields.io/github/repo-size/DefinetlyNotAI/Web_Scraper" alt="GitHub Repo Size"></a>
</div>

## Table of Contents

- [Installation](#-installation-and-setup-)
- [Usage](#basic-usage)
- [Functions Overview](#functions-overview)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation and Setup 🛠️

### Prerequisites

Ensure your system meets these requirements:

- Has Python 3.8 or higher.
- Downloaded all required dependencies.

### Step-by-Step Installation

1. **Clone the Repository**: Use Git to clone Web_Scraper to your local machine. Open Command Prompt as an administrator and run:

   ```powershell
   git clone https://github.com/DefinetlyNotAI/Web_Scraper.git
   ```

2. **Navigate to the Project Directory**: Change your current directory to the cloned CHANGE_ME folder:

   ```powershell
   cd Web_Scraper
   ```
   
3. **Install Dependencies**: Run `pip install -r requirements.txt`

4. **Run the Web Scraper**: Run `./scrape` more info below.


### Basic Usage


The utility is executed from the command line. Here's a basic example of how to use it:

```bash
python web_scraper.py --URL "https://example.com" --name "ExampleSite" --zip --full -y
```

### Options

- `--url`: Required. The URL of the website you wish to scrape.
- `--name`: Optional. A custom name for the scraped website. If not provided, the domain name will be used.
- `--zip`: Optional. If set, the utility will compress the downloaded files into a ZIP archive.
- `--full`: Optional. If set, the utility will download the full HTML content along with associated resources. Otherwise, it downloads only the basic HTML content.
- `-y`: Optional. Automatically proceeds with the download without asking for confirmation.

## Functions Overview

### `download_basic_html(url)`

Downloads the basic HTML content from a given URL and saves it to a file.

### `download_with_resources(url)`

Downloads the HTML content and associated resources from a given URL, saves them to a file, and returns the filename.

### `download_images(base_url, url)`

Downloads images from a given URL after processing them to get the absolute image URLs.

### `zip_files(zip_filename, files, delete_after=False)`

Zips the files given in the 'files' list into a zip file named 'zip_filename'. Optionally deletes the files after zipping.

### `parse()`

Main function that serves as the entry point for the web scraping application. Parses command-line arguments to scrape a given URL, download content based on the arguments provided, and optionally zip the downloaded files.

## Dependencies

- `argparse`: For parsing command-line options and arguments.
- `os`, `shutil`: For file and directory operations.
- `requests`: For making HTTP requests.
- `BeautifulSoup`: For parsing HTML content.
- `zipfile`: For creating ZIP archives.
- `tqdm`: For displaying progress bars during downloads.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

- [Source Code](https://github.com/DefinetlyNotAI/Web_Scraper)

Read the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
