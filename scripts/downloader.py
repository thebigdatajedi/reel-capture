#!/usr/bin/env python
import argparse
import os
import sys
import time
import yt_dlp
import logging
from threading import Thread
import urllib.parse as urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Spinner animation to indicate work in progress
def spinner() -> None:
    spin = ['|', '/', '-', '\\']
    idx = 0
    while True:
        sys.stdout.write(f"\rDownloading... {spin[idx % len(spin)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)


# Function to extract part of the URL for dynamic title
def get_page_name_from_url(url):
    try:
        parsed_url = urlparse.urlparse(url)
        custom_title = parsed_url.path.strip("/").split("/")[0]  # Get the first part of the path
        return custom_title
    except Exception as e:
        logging.error(f"Error parsing URL: {e}")
        return None


# Function to download video using yt-dlp with spinner animation
def download_video(video_url):
    output_dir = "downloaded_files"
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating directory '{output_dir}': {e}")
        return

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save in the downloaded_files directory
        'nocheckcertificate': True  # This disables SSL certificate verification
    }

    spinner_thread = Thread(target=spinner)
    spinner_thread.daemon = True
    spinner_thread.start()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            logging.info("Download complete.")
            logging.info(f"Video saved in the '{output_dir}' directory.")
    except Exception as e:
        logging.error(f"An error occurred during video download: {e}")
    finally:
        spinner_thread.join(timeout=0)


# Function to show usage information
def usage():
    logging.info("Usage: python downloader.py <facebook-url>")
    logging.info("Example: python downloader.py https://www.facebook.com/reel/2805384252954414")
    logging.info("Please provide a valid Facebook URL as an argument.")
    exit(1)


def main():
    parser = argparse.ArgumentParser(description='Download Facebook content by URL.')
    parser.add_argument('url', type=str, nargs='?', help='The Facebook URL to scrape content from')
    args = parser.parse_args()

    if not args.url:
        usage()

    video_url = args.url
    logging.info(f"Downloading video from URL: {video_url}")
    download_video(video_url)


if __name__ == "__main__":
    main()
