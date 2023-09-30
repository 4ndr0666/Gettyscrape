# Getty Video Scraper

## Overview

This Python script allows users to scrape and download videos from Getty Images based on a search term and a specified number of pages to scrape. It utilizes Selenium for web scraping and `tqdm` for a progress bar.

## Dependencies

- Selenium
- tqdm

## Installation

1. Clone this repository
    ```
    git clone https://github.com/4ndr0666/GettyScraper.git
    ```
  
2. Navigate to the cloned directory
    ```
    cd GettyScraper
    ```

3. Install the required packages
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the script
    ```
    python getty.js
    ```

2. Enter the search term and the number of pages to scrape when prompted.

## Output

The script will download the videos to a specified directory and provide a progress bar along with informative messages during the scraping process.

### Sample Output

Downloading: 17%|████████████▊ | 1/6 [00:03<00:18, 3.80s/it]

✔️ Downloaded video 1
...

## Features

- Real-time progress bar
- Handles exceptions and retries
- Downloads videos based on search term and number of pages

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Author

4ndr0666
