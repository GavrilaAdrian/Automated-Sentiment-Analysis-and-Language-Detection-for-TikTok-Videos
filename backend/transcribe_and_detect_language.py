import os
import whisper
from conversion import convert_mp4_to_wav
import gc
import torch
from typing import Tuple, Optional  # Ensure these are imported

# Transcribe and detect language
def transcriere_si_detectie_limbaj(video_link: str, VIDEO_DIR: str = 'database') -> Tuple[Optional[str], Optional[str]]:
    """
    Transcribes the audio from a video file and detects the language used.

    Args:
        video_link (str): The name of the video file to be processed.
        VIDEO_DIR (str): The directory where the video files are stored. Defaults to 'database'.

    Returns:
        Tuple[Optional[str], Optional[str]]:
            - The detected language as a string (e.g., "en" for English), or None if transcription fails.
            - The transcription of the video as a string, or None if transcription fails.
    """ 
    results = []
    
    # Use if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the Whisper model
    whisper_model = whisper.load_model("base", device=device, in_memory=True)
    
    try:
        video_path = os.path.join(VIDEO_DIR, video_link)
        wav_file = convert_mp4_to_wav(video_path)
        aux = whisper_model.transcribe(wav_file, task="transcribe")
        language, transcription = aux["language"], aux["text"]

        results.append({
            "language_detected": language,
            "transcription": transcription,
        })
    except Exception as e:
        print(f"Error transcribing {video_link}: {e}")

    # Cleanup
    del whisper_model
    gc.collect()

    if results:
        return results[0]['language_detected'], results[0]['transcription']
    else:
        return None, None
