This `README.md` will guide a research-centric user who is not as experienced with development but needs to run the script in the terminal. They will need to install the dependencies using Poetry and run the script with minimal interaction.

Facebook Video Downloader

## Overview

This script allows you to download videos or posts from public Facebook pages using Python. The script is designed for researchers or analysts who need to scrape and preserve valuable content from Facebook for research purposes.

The script includes:
- `downloader.py`: The main script for downloading content from Facebook.
- `test_downloader.py`: Unit tests to verify that the downloading function works correctly.

## Prerequisites

You will need to install the following before you can run the script:

- **Python 3.8 or above**: [Download Python here](https://www.python.org/downloads/).
- **Poetry** (dependency management tool): [Installation guide for Poetry](https://python-poetry.org/docs/#installation).
```bash
poetry install
```

This will create a virtual environment and install all necessary packages such as `facebook-scraper`, `youtube-dl`, and `pytest` for testing.

 Installation Instructions

### Step 1: Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/facebook-video-downloader.git
cd facebook-video-downloader
````

```bash
poetry run python scripts/downloader.py
```
### Step 2: Install Dependencies
Use **Poetry** to install the dependencies required for this project. In the terminal, run:


### Step 3: Run the Script
After installing the dependencies, you can run the script directly to download content from Facebook. Replace the URL in the script with the one you want to scrape.
### Step 4: Run the Tests
You can also run the provided tests to ensure the script is working as expected. These tests check that the scraper and page name extraction work properly.

```bash
poetry run pytest tests/test_downloader.py
```

## How to Use the Script

1. Open `downloader.py` and replace the `url` variable with the Facebook page or reel URL you wish to scrape content from.
2. Run the script, and it will download the video or posts.
3. The script will print the scraped data to the terminal.

### Example:
```python
url = "https://www.facebook.com/reel/2805384252954414"
```

## License

This project is licensed under the MIT License.
```
