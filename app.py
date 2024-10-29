import streamlit as st
import yt_dlp
import os
import uuid
import base64  # Ensure this import is present

# Function to set a permanent background image
def set_background(image_file):
    # Read the image and convert it to base64
    with open(image_file, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()
    
    # Apply the background image using CSS
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
                background-size: 100% auto;  /* Ensure the image fits mobile screen width */
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the permanent background image (adjust image name and location accordingly)
set_background('background_mobile.jpg')  # Ensure this image is in your project folder

# Function to download Facebook video
def download_facebook_video(fb_video_url):
    # Generate a unique filename using UUID
    unique_filename = f"downloaded_fb_video_{uuid.uuid4()}.mp4"
    
    # Set yt-dlp options with a unique output template
    ydl_opts = {
        'outtmpl': unique_filename,  # Save file with unique name
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,  # Ensure only the single video is downloaded
        'verbose': True  # Enable verbose output for debugging
    }

    try:
        st.write(f"Downloading from URL: {fb_video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return unique_filename
    except yt_dlp.utils.ExtractorError as e:
        return f"An error occurred: {str(e)}. Please ensure the URL is accessible and try again."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Streamlit UI
st.title("Abdullah Sajid's Facebook Downloader App")

# Get video URL from user input
video_url = st.text_input("Enter Facebook Video URL:")

# When the button is clicked, download the video
if st.button("Download"):
    if video_url:
        st.write(f"Attempting to download video from: {video_url}")
        output_file = download_facebook_video(video_url)
        if output_file.endswith('.mp4'):
            st.success(f"Download completed: {output_file}")
            # Provide a download button for the downloaded video
            with open(output_file, 'rb') as f:
                st.download_button("Download Video", f, file_name=output_file)
        else:
            st.error(output_file)  # Display the error message
    else:
        st.error("Please provide a Facebook video URL.")
