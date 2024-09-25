import streamlit as st
import yt_dlp
import os
import re
from urllib.parse import urlparse

def download_facebook_video(fb_video_url):
    # Extract video ID or generate a unique filename from the URL
    video_id_match = re.search(r'videos/(\d+)', fb_video_url)
    if video_id_match:
        video_id = video_id_match.group(1)
    else:
        video_id = "video"
    
    output_filename = f"downloaded_fb_video_{video_id}.mp4"

    # Set options for yt-dlp
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,
    }

    try:
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return output_filename
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Facebook Video Downloader App")

# Get video URL from user input
video_url = st.text_input("Enter Facebook Video URL:")

# Check if the video URL is valid and download on button click
if st.button("Download"):
    if video_url:
        parsed_url = urlparse(video_url)
        if not (parsed_url.scheme in ['http', 'https'] and 'facebook.com' in parsed_url.netloc):
            st.error("Please enter a valid Facebook video URL.")
        else:
            st.write(f"Downloading video from: {video_url}")
            output_file = download_facebook_video(video_url)
            if output_file.endswith('.mp4'):
                st.success(f"Download completed: {output_file}")
                with open(output_file, 'rb') as f:
                    st.download_button("Download Video", f, file_name=output_file)
            else:
                st.error(f"An error occurred: {output_file}")
    else:
        st.error("Please provide a Facebook video URL.")
