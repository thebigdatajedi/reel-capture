#!/usr/bin/env python
import argparse
import time
from unittest.mock import patch, MagicMock

import pytest
from scripts.downloader import get_page_name_from_url, download_video, spinner


# Test for URL parsing
def test_get_page_name_from_url():
    url = "https://www.facebook.com/reel/2805384252954414"
    page_name = get_page_name_from_url(url)
    assert page_name == "reel", f"Expected 'reel', but got '{page_name}'"


# Test for video downloading with a mock for yt-dlp
@patch('downloader.yt_dlp.YoutubeDL')  # Mock the YoutubeDL class from yt-dlp
def test_download_video(mock_yt_dlp):
    # Setup mock to simulate video download success
    mock_download_instance = MagicMock()
    mock_yt_dlp.return_value = mock_download_instance

    # Mock the os.makedirs function to avoid creating actual directories during tests
    with patch('os.makedirs') as mock_makedirs:
        # Call the function under test
        video_url = "https://www.facebook.com/reel/2805384252954414"
        download_video(video_url)

        # Ensure the correct directory was attempted to be created
        mock_makedirs.assert_called_once_with("downloaded_files", exist_ok=True)

        # Ensure the download function was called with the correct URL
        mock_download_instance.download.assert_called_once_with([video_url])


# Test for no URL passed (Branching in main() function)
@patch('downloader.usage')  # Mock the usage function
def test_no_url_passed(mock_usage):
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(url=None)):
        try:
            # Simulate the script being called with no URL
            import scripts
            scripts.downloader.main()
        except SystemExit:
            pass  # Handle the sys.exit() call gracefully

        # Ensure that the usage function was called
        mock_usage.assert_called_once()


# Test for video download failure (Branching in download_video())
@patch('downloader.yt_dlp.YoutubeDL')  # Mock the YoutubeDL class
def test_download_video_failure(mock_yt_dlp):
    # Setup mock to simulate a download failure
    mock_download_instance = MagicMock()
    mock_download_instance.download.side_effect = Exception("Download failed")
    mock_yt_dlp.return_value = mock_download_instance

    # Call the function under test with a mock
    with patch('os.makedirs'):
        video_url = "https://www.facebook.com/reel/2805384252954414"
        download_video(video_url)

        # Ensure the download function was called and the error was handled
        mock_download_instance.download.assert_called_once_with([video_url])


# Test for spinner loop (Looping in spinner function)
@patch('sys.stdout.write')  # Mock the output to avoid actual console printing
@patch('time.sleep', return_value=None)  # Mock sleep to break the loop
def test_spinner(mock_sleep, mock_stdout):
    # Create a short-lived spinner loop by running the spinner in a separate thread
    from threading import Thread

    def run_spinner():
        spinner()  # Spinner runs indefinitely, but we will simulate breaking out

    thread = Thread(target=run_spinner)
    thread.start()

    # Let the spinner run for a short while
    time.sleep(0.3)

    # Ensure the spinner was updating the terminal output
    assert mock_stdout.call_count > 1  # Ensure spinner called multiple times

    # Stop the thread to end the test
    thread.join(timeout=0)


# Run tests
if __name__ == "__main__":
    pytest.main()
