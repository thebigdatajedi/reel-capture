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


# Test for video download failure
@patch('scripts.downloader.yt_dlp.YoutubeDL.__enter__')
def test_download_video_failure(mock_yt_dlp_enter):
    # Setup mock to simulate a download failure
    mock_download_instance = MagicMock()
    mock_download_instance.download.side_effect = Exception("Download failed")
    mock_yt_dlp_enter.return_value = mock_download_instance

    # ... rest of your test code

    # Ensure the download function was called and the error was handled
    mock_download_instance.download.assert_called_once_with([video_url])


@patch('scripts.downloader.usage')  # Correct path to where usage() is used
def test_no_url_passed(mock_usage):
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(url=None)):
        try:
            # Simulate the script being called with no URL
            import scripts.downloader
            scripts.downloader.main()
        except SystemExit:
            pass  # Handle the sys.exit() call gracefully

        # Ensure that the usage function was called
        mock_usage.assert_called_once()


# Test for spinner loop (Looping in spinner function)
@patch('sys.stdout.write')  # Mock the output to avoid actual console printing
@patch('time.sleep', return_value=None)  # Mock sleep to break the loop
def test_spinner(mock_sleep, mock_stdout):
    # Call the spinner with a maximum of 5 cycles for testing
    spinner(max_cycles=50)

    # Ensure the spinner was updating the terminal output
    assert mock_stdout.call_count >= 1  # Ensure spinner called at least once


# Run tests
if __name__ == "__main__":
    pytest.main()
