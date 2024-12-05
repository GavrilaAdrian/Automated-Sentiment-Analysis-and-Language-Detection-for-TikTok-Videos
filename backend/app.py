from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import pyktok as pyk
import os
import shutil
import csv
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from translate_and_sentiment import translate_text, get_sentiment
from transcribe_and_detect_language import transcriere_si_detectie_limbaj
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
if not MONGODB_CONNECTION_STRING:
    raise ValueError("MongoDB connection string is missing from the .env file.")

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client["tiktok_database"]
collection = db["tiktoks"]

search_query = "raiffeisen"
linkNumbers = 2

generate_Data = False
create_Json = True

def save_tiktok(link: str, output_dir: str = 'database', datafile: str = 'data.csv') -> None:
    """
    Download a TikTok video and move it to the specified directory.

    Args:
        link (str): The TikTok video URL.
        output_dir (str): The directory to save the video. Defaults to 'database'.
        datafile (str): The path to the CSV file to save metadata. Defaults to 'data.csv'.
    """
    # Download the video and data
    pyk.save_tiktok(link, True, datafile)
    video_filename = link.replace('https://www.tiktok.com/', '').replace('/', '_') + '.mp4'  # Get video name

    # Create the 'output_dir' directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Move video to the directory
    video_path = os.path.join(output_dir, video_filename)
    shutil.move(video_filename, video_path)

def fetch_tiktok_video_urls(
    search_query: str,
    num_links: int = 10,
    file_path: str = 'links.txt',
    create_file: bool = True
) -> List[str]:
    """
    Fetch TikTok video URLs based on a search query.

    Args:
        search_query (str): The search query.
        num_links (int): The number of video links to fetch. Defaults to 10.
        file_path (str): The file path to save the URLs. Defaults to 'links.txt'.
        create_file (bool): Whether to create a file with the URLs. Defaults to True.

    Returns:
        List[str]: A list of video URLs.
    """
    base_url = f"https://www.tiktok.com/tag/{search_query}"

    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--disable-webrtc")
    edge_options.add_argument("--lang=ro")  # Set browser language to Romanian
    edge_options.add_argument("--accept-lang=ro-RO,ro;q=0.9")
    edge_options.add_argument("--default-search-engine=Google")
    edge_options.add_argument("--default-search-engine-url=https://www.google.ro")

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)
    driver.get(base_url)

    # Wait for the page to load
    time.sleep(20)

    # Scroll to load more videos
    for _ in range(num_links // 15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # Find video links
    video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
    video_urls = [element.get_attribute('href') for element in video_elements[:2 * num_links]]
    video_urls = [url for i, url in enumerate(video_urls) if i % 2 == 0]

    if create_file:
        with open(file_path, 'w') as file:
            for url in video_urls:
                file.write(url + '\n')

    driver.quit()
    return video_urls

def organize_data_from_csv(
    datafile: str = 'data.csv',
    output_dir: str = 'database'
) -> List[Dict[str, str]]:
    """
    Process data from a CSV file, adding translations, transcriptions, and sentiment analysis.

    Args:
        datafile (str): The CSV file path containing the data. Defaults to 'data.csv'.
        output_dir (str): The directory containing video files. Defaults to 'database'.

    Returns:
        List[Dict[str, str]]: A list of processed video data dictionaries.
    """    
    data = []
    with open(datafile, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Add the video_file field
            file_name = f"@{row['author_username']}_video_{row['video_id']}.mp4"
            video_path = os.path.join(output_dir, file_name)
            print(video_path)
            language, transcription = transcriere_si_detectie_limbaj(file_name)  # Language detected and transcription
            print(f"Detected language: {language}, transcription: {transcription}")
            print(row)
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')
            # Add translation, sentiment, and other fields
            if transcription is not None:
                sentence = translate_text(transcription, language)
                score = get_sentiment(transcription, language)

                row['language'] = language
                row['sentence'] = sentence
                row['sentiment_score'] = score
                row['video_file'] = video_path

                # Remove useless columns from the row
                del row['video_diggcount']
                del row['video_description']
                del row['video_stickers']
                del row['author_diggcount']
                del row['poi_name']
                del row['poi_address']
                del row['poi_city']

                # Append to data list
                data.append(row)

    return data  # Return the data as a list of dictionaries


def save_to_mongodb(data: List[Dict[str, str]]) -> None:
    """
    Save processed video data to MongoDB.

    Args:
        data (List[Dict[str, str]]): A list of processed video data dictionaries.
    """
    try:
        if isinstance(data, list):
            replaced_count = 0
            new_count = 0

            for document in data:
                # Perform an upsert to replace existing documents or insert new ones
                result = collection.update_one(
                    {"video_id": document["video_id"]},  # Match by video_id
                    {"$set": document},                 # Replace with the new data
                    upsert=True                         # Insert if no document matches
                )

                # Track updates vs inserts
                if result.matched_count > 0:
                    replaced_count += 1  # Document was replaced
                else:
                    new_count += 1  # New document was inserted

            print(f"Replaced {replaced_count} existing documents.")
            print(f"Inserted {new_count} new documents.")
        else:
            print("Data is not in the correct format for MongoDB.")
    except Exception as e:
        print(f"An error occurred while saving to MongoDB: {e}")

# Use this method to delete everything from the data.csv file, except the first row
def keep_header_only(file_path: str) -> None:
    """
    Retain only the header row in a CSV file for processing only the fetched tiktoks.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Read the first row (header) from the file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the first row

        # Overwrite the file with only the header
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header back

        print(f"All rows except the header have been deleted from '{file_path}'.")

    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
keep_header_only('data.csv')


# Example usage
if __name__ == "__main__":
    if generate_Data:
        urls = fetch_tiktok_video_urls(search_query, num_links=linkNumbers, create_file=False)  # Generate linkNumbers URLs
        for url in urls:
            save_tiktok(url)  # Save video files and metadata
        print(urls)
    if create_Json:  # Don't run this code without the data.csv file
        data = organize_data_from_csv()  # Create data with sentiment, transcription, and translation
        with open('data_json.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # Convert the list to a JSON-formatted string
        save_to_mongodb(data)  # Save JSON data to MongoDB
