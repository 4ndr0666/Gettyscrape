from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import os
from tqdm import tqdm

# Symbols for Visual Feedback
SUCCESS = "✔️"
FAILURE = "❌"
EXPLOSION = "💥"

def download_media(search_term, src, seq, dir, media_type):
    try:
        ext = "jpg"
        filename = f"{search_term}_{seq}.{ext}"
        media_path = os.path.join(dir, filename)
        urllib.request.urlretrieve(src, media_path)
        print(f"{SUCCESS} Downloaded picture {seq + 1}")
    except Exception as e:
        print(f"{FAILURE} Download failed: {e}")

def get_media_from_getty(driver, search_term, pages, dir, media_type):
    seq = 0
    wait = WebDriverWait(driver, 10)
    for i in range(1, pages + 1):
        url = f"https://www.gettyimages.com/photos/{search_term}?page={i}"
        driver.get(url)

        try:
            all_images = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article//img")))
        except:
            print(f"Timeout reached for page {i}, skipping...")
            continue

        for img in all_images:
            try:
                # Construct high-resolution image URL
                img_src = img.get_attribute("src")
                high_res_src = img_src.split('?')[0] + '?s=2048x2048&w=5'
                download_media(search_term, high_res_src, seq, dir, media_type)
                seq += 1
            except Exception as e:
                print(f"Error downloading picture: {e}")

    print(f"{EXPLOSION} Scraping complete. {EXPLOSION}")
    print(f"Total pictures downloaded: {seq}")

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

