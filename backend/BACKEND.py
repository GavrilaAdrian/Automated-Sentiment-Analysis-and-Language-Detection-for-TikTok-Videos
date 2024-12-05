from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from app import save_tiktok, fetch_tiktok_video_urls, organize_data_from_csv, save_to_mongodb, keep_header_only
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# MongoDB connection setup
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
if not MONGODB_CONNECTION_STRING:
    raise ValueError("MONGODB_CONNECTION_STRING is not set in the .env file.")

client = MongoClient(MONGODB_CONNECTION_STRING)
db = client["tiktok_database"]
tiktoks_collection = db["tiktoks"]

@app.route('/process', methods=['POST'])
def process_videos() -> Any:
    """
    Endpoint to process TikTok videos. It fetches video URLs, processes metadata,
    and saves the data to MongoDB.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    count = data.get('count', 1)  # Default to 1 video if not specified
    count = min(max(1, count), 100)  # Restrict to range 1–100
    
    try:
        # Step 1: Fetch TikTok video URLs
        video_urls = fetch_tiktok_video_urls(search_query="raiffeisen", num_links=count)
        
        # Step 2: Save each TikTok video and its metadata
        for url in video_urls:
            save_tiktok(url)
            
        # Step 3: Organize data from CSV and process language, transcription, sentiment
        processed_videos = organize_data_from_csv()

        # Step 4: Save processed videos to MongoDB
        save_to_mongodb(processed_videos)
        
        # Step 5: Empty data.csv
        keep_header_only('data.csv')
        
        return jsonify({"message": f"{count} videos processed and stored"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/videos', methods=['GET'])
def get_processed_videos() -> Any:
    """
    Endpoint to fetch processed TikTok videos from MongoDB.

    Returns:
        JSON response containing the list of processed videos.
    """
    try:
        print("Fetching videos from MongoDB...")
        videos = list(tiktoks_collection.find({}, {
            "_id": 0,                     # Exclude MongoDB ID from the response
            "video_id": 1,                # Include video_id
            "video_file": 1,              # Include video_file
            "author_name": 1,             # Include author_name
            "author_username": 1,         # Include author_username
            "video_playcount": 1,         # Include video_playcount
            "sentiment_score": 1,         # Include sentiment_score
            "language": 1,                # Include language
            "video_timestamp": 1          # Include video_timestamp for sorting
        }))

        # Deduplicate by `video_id` and sort by timestamp
        unique_videos = sorted(
            {video["video_id"]: video for video in videos}.values(),
            key=lambda x: x["video_timestamp"]  # Sort by timestamp (ascending)
        )

        response = {
            "total_videos": len(unique_videos),  # Total count of unique videos
            "processed_videos": list(unique_videos)  # Deduplicated and sorted videos
        }

        print(f"Fetched {len(response['processed_videos'])} unique videos.")
        return jsonify(response), 200
    except Exception as e:
        print(f"Error in /videos: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/video/<video_id>', methods=['GET'])
def get_video_details(video_id: str) -> Any:
    """
    Endpoint to fetch detailed information about a specific video by its video_id.

    Args:
        video_id (str): The ID of the video to fetch.

    Returns:
        JSON response containing the video details or an error message if not found.
    """
    try:
        # Query the database to fetch the video details by video_id
        video = tiktoks_collection.find_one(
            {"video_id": video_id},  # Match the video_id field
            {
                "_id": 0,  # Exclude the MongoDB Object ID
                "video_id": 1,
                "video_file": 1,
                "video_timestamp": 1,
                "video_duration": 1,
                "video_playcount": 1,
                "video_sharecount": 1,
                "video_is_ad": 1,
                "author_name": 1,
                "author_username": 1,
                "author_followercount": 1,
                "author_videocount": 1,
                "author_verified": 1,
                "language": 1,
                "sentence": 1,
                "sentiment_score": 1,
            }
        )

        # If no video is found, return a 404 response
        if not video:
            return jsonify({"error": "Video not found"}), 404

        # Return the video details
        return jsonify(video), 200

    except Exception as e:
        # Catch and return any errors
        print(f"Error in /video/{video_id} endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# For displaying video on DetailsPage.tsx
@app.route('/video-files/<filename>')
def serve_video_file(filename: str) -> Any:
    """
    Endpoint to serve video files by filename.

    Args:
        filename (str): The name of the video file to serve.

    Returns:
        The video file as a response.
    """
    return send_from_directory('database', filename)

if __name__ == "__main__":
    app.run(debug=True)
