from moviepy.editor import VideoFileClip, AudioFileClip
from pytube import YouTube
import os
import re

# Create a directory for downloads if it doesn't exist
download_dir = "./downloads"
os.makedirs(download_dir, exist_ok=True)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

url = input("Enter the video URL you are interested in downloading:\n\n")

try:
    yt = YouTube(url)

    print(f"Title: {yt.title}")
    print(f"Thumbnail URL: {yt.thumbnail_url}")

    # Sanitize the video title for the filename
    sanitized_title = sanitize_filename(yt.title)

    # Download video and audio separately
    video_stream = yt.streams.get_by_itag(248)
    audio_stream = yt.streams.get_by_itag(140)
    
    if not video_stream or not audio_stream:
        print("The specified itags do not exist for this video. Please check the available streams.")
    else:
        video_path = video_stream.download(output_path=download_dir, filename="video.mp4")
        audio_path = audio_stream.download(output_path=download_dir, filename="audio.mp3")

        # Load the video and audio files
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set the audio of the video clip
        final_video = video.set_audio(audio)

        # Save the final video
        final_video_path = os.path.join(download_dir, f"{sanitized_title}.mp4")
        final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')
        os.remove("./downloads/video.mp4")
        os.remove("./downloads/audio.mp3")
        print(f"Final video saved at: {final_video_path}")

except Exception as e:
    print(f"An error occurred: {e}")


