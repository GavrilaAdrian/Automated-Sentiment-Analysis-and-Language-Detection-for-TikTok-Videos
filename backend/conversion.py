from moviepy.video.io.VideoFileClip import VideoFileClip

def convert_mp4_to_wav(mp4_file_path, wav_file_path = 'output.wav'):
    video_clip = VideoFileClip(mp4_file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_file_path)
    return wav_file_path
