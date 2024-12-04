import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the MongoDB URI
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
if not MONGODB_CONNECTION_STRING:
    raise ValueError("MongoDB connection string is missing from the .env file.")

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client["tiktok_database"]  # Connect to the correct database
collection = db["tiktoks"]  # Specify the correct collection

# Folder containing the TikTok videos
folder_path = "../database"

# Iterate through all video files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".mp4"):  # Only process MP4 files
        # Extract the video ID from the filename
        video_id = filename.split("_video_")[-1].replace(".mp4", "")

        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Update the MongoDB document with the file path
        result = collection.update_one(
            {"video_id": video_id},  # Find the document by video ID
            {"$set": {"video_file_path": file_path}}  # Add or update the file path field
        )

        # Print the result of the update operation
        if result.matched_count > 0:
            print(f"Updated document for video ID {video_id} with file path: {file_path}")
        else:
            print(f"No document found for video ID {video_id}. Skipped.")

# Close the MongoDB connection
mongo_client.close()
