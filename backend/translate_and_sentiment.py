import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text: str, target_language: str) -> str | None:
    """
    Translates the given text from the specified target language into English.
    
    Args:
        text (str): The text to be translated.
        target_language (str): The language of the input text.
        
     Returns:
        str | None: The translated text in English, or None if an error occurs.
    
    """
    try:
        # Construct the prompt for translation
        prompt = (
            f"Translate the following text from {target_language} in English:\n\n"
            f"{text}"
        )

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful translator which only translates in English the same exact text. "
                        f"The text is most probably in {target_language}."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=1000,
        )

        # Extract the translated text
        translated_text = response.choices[0].message.content
        return translated_text
    except Exception as e:
        print(f"Error in translation: {e}")
        return None

def get_sentiment(text: str, target_language: str) -> str | None:
    """
    Analyzes the sentiment of the given text and returns a rating between 0 and 100.

     The sentiment rating represents the impact of the text on Raiffeisen Bank:
    - 0 indicates the text damages the company's image or trustability.
    - 100 indicates the text improves the company's image or trustability.
    - 50 is used for neutral or incomprehensible text.

    Args:
        text (str): The text to be analyzed.
        target_language (str): The language of the input text.
        
    Returns:
        str | None: A numeric rating (0-100) as a string, or None if an error occurs.
    """
    try:
        # Construct the prompt for sentiment analysis
        prompt = (
            f"Analyze the sentiment of the following text and return the damage and trustability rating: {text}\n\n"
        )

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant which will determine how the provided texts "
                        "about Raiffeisen Bank impact the company. You will rate the impact from 0 to 100. "
                        "0 means the text damages the image or trustability of the company, "
                        "100 means the text improves the image or trustability of the company. "
                        "There might be texts where there are song lyrics or no comprehensible text, "
                        "in this case you should rate the text with 50. "
                        f"The text is most probably in {target_language}. "
                        "Your response has to be only a number between 0 and 100, nothing else."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=1000,
        )

        # Extract the sentiment rating
        rated_text = response.choices[0].message.content
        print("______________________________________________________________________________")
        print(rated_text)
        print("______________________________________________________________________________")
        return rated_text
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return None
