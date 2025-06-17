import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Load proxy settings from Streamlit secrets
PROXIES = {
    "http": st.secrets["proxy_http"],
    "https": st.secrets["proxy_https"]
}

def extract_video_id(url):
    patterns = [
        r"youtu\.be/([^\?&]+)",
        r"youtube\.com/watch\?v=([^\?&]+)",
        r"youtube\.com/embed/([^\?&]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_spanish_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=PROXIES)
        transcript = transcript_list.find_transcript(['es']).fetch()
        return transcript, None
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return None, "No Spanish transcript found for this video."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
