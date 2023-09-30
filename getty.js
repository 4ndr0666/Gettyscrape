from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import time
import os
from tqdm import tqdm  # For the progress bar

# Symbols for Visual Feedback
SUCCESS = "✔️"
FAILURE = "❌"
EXPLOSION = "💥"

def download_video(search_term, src, seq, dir):
    try:
        filename = f"{search_term}_{seq}.mp4"
        video_path = os.path.join(dir, filename)
        urllib.request.urlretrieve(src, video_path)
        print(f"{SUCCESS} Downloaded video {seq + 1}")
    except Exception as e:
        print(f"{FAILURE} Download failed: {e}")

def get_videos_from_getty(driver, search_term, pages, dir):
    seq = 0
    wait = WebDriverWait(driver, 10)
    for i in range(1, pages + 1):
        url = f"https://www.gettyimages.com/videos/{search_term}?page={i}"
        driver.get(url)
        
        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
        except:
            print(f"Timeout reached for page {i}, skipping...")
            continue

        thumbnails = driver.find_elements(By.XPATH, "//article")
        
        for idx in tqdm(range(len(thumbnails)), desc=f"Downloading", bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[36m", "\033[0m")):
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    thumbnails = driver.find_elements(By.XPATH, "//article")
                    thumbnails[idx].click()
                    video = wait.until(EC.presence_of_element_located((By.XPATH, "//video")))
                    src = video.get_attribute("src")
                    download_video(search_term, src, seq, dir)
                    seq += 1
                    break
                except Exception as e:
                    retries += 1
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))

    print(f"{EXPLOSION} Scraping complete. {EXPLOSION}")
    print(f"Total videos downloaded: {seq}")

if __name__ == '__main__':
    search_term = input("Search term: ")
    pages = int(input("Number of pages to scrape: "))
    user = os.environ['USER']
    dir = f"/home/{user}/Getty/"

    if not os.path.isdir(dir):
        os.makedirs(dir)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    get_videos_from_getty(driver, search_term, pages, dir)
    driver.quit()
