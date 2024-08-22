from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


import re
from urllib.parse import urlparse, parse_qs

def get_youtube_id(url):
    # Patterns for different types of YouTube URLs
    patterns = [
        r'^https?:\/\/(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'^https?:\/\/(?:www\.)?youtube\.com\/embed\/([^?]+)',
        r'^https?:\/\/(?:www\.)?youtube\.com\/v\/([^?]+)',
        r'^https?:\/\/youtu\.be\/([^?]+)',
        r'^https?:\/\/(?:www\.)?youtube\.com\/shorts\/([^?]+)',
        r'^https?:\/\/(?:www\.)?youtube\.com\/live\/([^?]+)'
    ]

    # Try to match the URL against each pattern
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)

    # If no pattern matches, try parsing the URL
    parsed_url = urlparse(url)
    if parsed_url.netloc in ('youtube.com', 'www.youtube.com'):
        query = parse_qs(parsed_url.query)
        if 'v' in query:
            return query['v'][0]

    # If we still haven't found an ID, raise an exception
    raise ValueError("Could not extract YouTube video ID from URL")

def get_youtube_transcript(url):
    try:
        # Extract video ID from the URL
        video_id = get_youtube_id(url)
        
        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text parts
        full_transcript = " ".join([entry['text'] for entry in transcript])
        
        return full_transcript
    except ValueError as e:
        raise ValueError(f"Invalid YouTube URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching YouTube transcript: {str(e)}")