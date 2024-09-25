import streamlit as st
import yt_dlp
import base64
import os
import re
from urllib.parse import urlparse

# Function to set a permanent background image
def set_background(image_file):
    with open(image_file, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        @media (max-width: 600px) {{
            .stApp {{
                background-size: 100% auto;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background
set_background('background_mobile.jpg')

st.title("Abdullah Sajid's Facebook Video Downloader App")

# Function to download Facebook video
def download_facebook_video(fb_video_url):
    # Create a valid filename by replacing special characters
    video_id = re.search(r'(?<=videos/)(\d+)', fb_video_url)
    if video_id:
        output_filename = f'downloaded_fb_video_{video_id.group(0)}.mp4'
    else:
        output_filename = 'downloaded_fb_video.mp4'
    
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return output_filename
    except Exception as e:
        return str(e)

# Input field for video URL
video_url = st.text_input("Enter Facebook Video URL:")

if st.button("Download"):
    if video_url:
        # Validate URL
        parsed_url = urlparse(video_url)
        if not (parsed_url.scheme in ['http', 'https'] and 'facebook.com' in parsed_url.netloc):
            st.error("Please enter a valid Facebook video URL.")
        else:
            output_file = download_facebook_video(video_url)
            if output_file.endswith('.mp4'):
                st.success("Download completed!")
                with open(output_file, 'rb') as f:
                    st.download_button("Download Video", f, file_name=output_file)
            else:
                st.error(f"An error occurred: {output_file}")
                if "Cannot parse data" in output_file:
                    st.warning("This may be a temporary issue with Facebook. Please try updating yt-dlp or try again later.")
