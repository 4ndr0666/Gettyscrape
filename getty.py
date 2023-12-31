from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import time
import os
from tqdm import tqdm

# Symbols for Visual Feedback
SUCCESS = "✔️"
FAILURE = "❌"
EXPLOSION = "💥"

def download_media(search_term, src, seq, dir, media_type):
    try:
        ext = "mp4" if media_type == "video" else "jpg"
        filename = f"{search_term}_{seq}.{ext}"
        media_path = os.path.join(dir, filename)
        urllib.request.urlretrieve(src, media_path)
        print(f"{SUCCESS} Downloaded {media_type} {seq + 1}")
    except Exception as e:
        print(f"{FAILURE} Download failed: {e}")

def get_media_from_getty(driver, search_term, pages, dir, media_type):
    seq = 0
    wait = WebDriverWait(driver, 10)
    for i in range(1, pages + 1):
        url = f"https://www.gettyimages.com/{'videos' if media_type == 'video' else 'photos'}/{search_term}?page={i}"
        driver.get(url)

        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
        except:
            print(f"Timeout reached for page {i}, skipping...")
            continue

        media_elements = driver.find_elements(By.XPATH, "//article")

        for idx in tqdm(range(len(media_elements)), desc=f"Downloading {media_type}s"):
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    media_elements = driver.find_elements(By.XPATH, "//article")
                    media_elements[idx].click()
                    media = wait.until(EC.presence_of_element_located((By.XPATH, "//video" if media_type == "video" else "//img")))
                    src = media.get_attribute("src")
                    download_media(search_term, src, seq, dir, media_type)
                    seq += 1
                    break
                except Exception as e:
                    retries += 1
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))

    print(f"{EXPLOSION} Scraping complete. {EXPLOSION}")
    print(f"Total {media_type}s downloaded: {seq}")

if __name__ == '__main__':
    search_term = input("Search term: ")
    media_type = input("Download videos or pictures? (Type 'video' or 'picture'): ").lower()
    pages = int(input("Number of pages to scrape: "))
    user = os.environ['USER']
    dir = f"/home/{user}/Getty/"

    if not os.path.isdir(dir):
        os.makedirs(dir)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    get_media_from_getty(driver, search_term, pages, dir, media_type)
    driver.quit()
