import streamlit as st
import yt_dlp
import base64

# Function to set permanent background image
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

# Set the permanent background image
set_background('background_mobile.jpg')  # Background image saved as 'background_mobile.jpg' in your project folder

st.title("Abdullah Sajid's Facebook Video Downloader App")

# Function to download Facebook video
def download_facebook_video(fb_video_url, output_path='./downloaded_fb_video.mp4'):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'restrictfilenames': True,
        'noplaylist': True,
    }
    
    try:
        part_file = output_path + ".part"
        if os.path.exists(part_file):
            os.remove(part_file)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_video_url])
        return output_path
    except Exception as e:
        return str(e)

# Main Video Downloader Interface
video_url = st.text_input("Enter Facebook Video URL:")

if st.button("Download"):
    if video_url:
        output_file = download_facebook_video(video_url)
        if output_file.endswith('.mp4'):
            st.success("Download completed!")
            with open(output_file, 'rb') as f:
                st.download_button("Download Video", f, file_name="downloaded_fb_video.mp4")
        else:
            st.error(f"An error occurred: {output_file}")
