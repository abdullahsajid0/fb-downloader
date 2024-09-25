import streamlit as st
import yt_dlp
import os
import re
from urllib.parse import urlparse

def download_facebook_video(fb_video_url):
    # Extract video ID or create unique filename from the URL
    video_id_match = re.search(r'videos/(\d+)', fb_video_url)
    
    if video_id_match:
        video_id = video_id_match.group(1)
    else:
        video_id = "default_video"  # fallback if no ID found
    
    output_filename = f"downloaded_fb_video_{video_id}.mp4"

    # Set yt-dlp options
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,
    }

    try:
        st.write(f"Downloading from URL: {fb_video_url}")  # Debug print URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return output_filename
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Facebook Video Downloader App")

# Get video URL from user input
video_url = st.text_input("Enter Facebook Video URL:")

# When the button is clicked, download the video
if st.button("Download"):
    if video_url:
        parsed_url = urlparse(video_url)
        if not (parsed_url.scheme in ['http', 'https'] and 'facebook.com' in parsed_url.netloc):
            st.error("Please enter a valid Facebook video URL.")
        else:
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
