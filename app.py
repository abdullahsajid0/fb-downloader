import streamlit as st
import yt_dlp
import os
import uuid
from datetime import datetime

def download_facebook_video(fb_video_url):
    # Generate a unique filename using timestamp or UUID
    unique_filename = f"downloaded_fb_video_{uuid.uuid4()}.mp4"
    
    # Set yt-dlp options with a unique output template
    ydl_opts = {
        'outtmpl': unique_filename,  # Save file with unique name
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,  # Ensure only the single video is downloaded
    }

    try:
        st.write(f"Downloading from URL: {fb_video_url}")  # Debug: Print the URL being downloaded
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return unique_filename
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Abdullah Sajid's Facebook Downloader App")

# Get video URL from user input
video_url = st.text_input("Enter Facebook Video URL:")

# When the button is clicked, download the video
if st.button("Download"):
    if video_url:
        st.write(f"Attempting to download video from: {video_url}")  # Debugging URL before download
        output_file = download_facebook_video(video_url)
        if output_file.endswith('.mp4'):
            st.success(f"Download completed: {output_file}")
            with open(output_file, 'rb') as f:
                st.download_button("Download Video", f, file_name=output_file)
        else:
            st.error(f"An error occurred: {output_file}")
    else:
        st.error("Please provide a Facebook video URL.")
