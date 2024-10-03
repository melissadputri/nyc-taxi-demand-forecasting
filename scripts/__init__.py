import os
import time
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URL of the NYC TLC Trip Record Data page
BASE_URL = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

# Define the paths for the 'landing', 'raw', and 'curated' folders relative to the script's location
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
LANDING_FOLDER = os.path.join(DATA_FOLDER, "landing")
RAW_FOLDER = os.path.join(DATA_FOLDER, "raw")
CURATED_FOLDER = os.path.join(DATA_FOLDER, "curated")

# Create the directories if they do not exist
os.makedirs(LANDING_FOLDER, exist_ok=True)
os.makedirs(RAW_FOLDER, exist_ok=True)
os.makedirs(CURATED_FOLDER, exist_ok=True)

print(f"Created or confirmed existence of directories:\n- {LANDING_FOLDER}\n- {RAW_FOLDER}\n- {CURATED_FOLDER}")

def get_parquet_links():
    """
    Use Selenium to scrape the TLC trip record data page for PARQUET links
    for HVFHV trip records from June 2023 to May 2024.
    """
    # Set up Selenium WebDriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Open the webpage
    driver.get(BASE_URL)
    time.sleep(3)  # Allow time for the page to load

    # Find all <a> tags with class 'exitlink'
    links = driver.find_elements(By.CLASS_NAME, "exitlink")
    
    # Extract PARQUET links for the desired time range (June 2023 to May 2024)
    parquet_links = []
    shapefile_link = None
    for link in links:
        href = link.get_attribute("href")
        if href and "fhvhv_tripdata_" in href and href.endswith(".parquet"):
            href = href.strip()  # Trim any extra spaces
            # Extract year and month from the filename
            year_month = href.split("fhvhv_tripdata_")[1].split(".parquet")[0]
            year, month = map(int, year_month.split('-'))

            # Filter for June 2023 to May 2024
            if (year == 2023 and month >= 6) or (year == 2024 and month <= 5):
                parquet_links.append(href)
        elif href and "taxi_zones.zip" in href:
            shapefile_link = href.strip()  # Found the shapefile link

    # Close the browser
    driver.quit()
    
    return parquet_links, shapefile_link

def download_file(url, save_path):
    """
    Download a file from the given URL and save it to the specified path.
    """
    print(f"Downloading {save_path}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Saved {save_path}.")

def unzip_file(zip_path, extract_to):
    """
    Unzip a ZIP file to the specified directory.
    """
    print(f"Unzipping {zip_path} to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Unzipped {zip_path}.")

if __name__ == "__main__":
    print("Scraping PARQUET links with Selenium...")
    parquet_links, shapefile_link = get_parquet_links()
    
    print(f"Found {len(parquet_links)} PARQUET files.")
    
    print("Starting download of PARQUET files...")
    for url in parquet_links:
        filename = os.path.join(LANDING_FOLDER, url.split("/")[-1])
        download_file(url, filename)
    
    if shapefile_link:
        print("Starting download of the shapefile...")
        shapefile_filename = os.path.join(LANDING_FOLDER, shapefile_link.split("/")[-1])
        download_file(shapefile_link, shapefile_filename)
        
        # Automatically unzip the shapefile
        unzip_file(shapefile_filename, LANDING_FOLDER)
    
    print("All files downloaded and processed successfully.")
