# scrape_signasl_org.py

import requests
from bs4 import BeautifulSoup
import os
import csv
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the base URL
base_url = "https://www.signasl.org"

# Define the directory to save the videos and metadata
save_directory = r"C:\Users\toddk\Documents\ASL_Videos"
os.makedirs(save_directory, exist_ok=True)

# Path for metadata CSV
metadata_csv_path = os.path.join(save_directory, "metadata.csv")

# Function to download a video
def download_video(video_url, save_path):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"Downloaded: {save_path}")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

# Function to scrape and download videos
def scrape_and_download(word_list):
    metadata = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for word in word_list:
            if word.lower().startswith('a'):
                logging.info(f"Processing word: {word}")
                sign_page_url = f"{base_url}/sign/{word}"
                futures.append(executor.submit(process_word, word, sign_page_url, metadata))
        
        for future in futures:
            future.result()
    
    # Save metadata to a CSV file
    with open(metadata_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['word', 'video_url', 'save_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for data in metadata:
            writer.writerow(data)

# Function to process a single word
def process_word(word, sign_page_url, metadata):
    try:
        response = requests.get(sign_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <video> tags
        video_tags = soup.find_all('video')
        if video_tags:
            for idx, video_tag in enumerate(video_tags, start=1):
                source_tag = video_tag.find('source')
                if source_tag and 'src' in source_tag.attrs:
                    video_url = source_tag['src']
                    # Construct save path with index
                    video_filename = f"{word}_{idx}.mp4"
                    save_path = os.path.join(save_directory, video_filename)
                    # Check if the file already exists
                    if os.path.exists(save_path):
                        logging.info(f"File already exists: {save_path}")
                    else:
                        # Download the video
                        download_video(video_url, save_path)
                        # Extract metadata
                        metadata.append({
                            "word": word,
                            "video_url": video_url,
                            "save_path": save_path
                        })
        else:
            logging.info(f"No video found for: {word}")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    
    # Add a small delay between requests
    time.sleep(1)

# Function to read all words starting with "a" or "A" from a file
def read_words_starting_with_a(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return [line.strip() for line in file if line.strip().lower().startswith('a')]

# Main function to scrape words starting with "a" or "A"
def scrape_words_starting_with_a(file_path):
    words = read_words_starting_with_a(file_path)
    scrape_and_download(words)

# Run the script
input_file_path = r"C:\Users\toddk\Documents\The_Oxford_3000_cleaned.txt"
scrape_words_starting_with_a(input_file_path)
