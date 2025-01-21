from googleapiclient.discovery import build
import yt_dlp
from moviepy.editor import VideoFileClip

API_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search_creative_commons_gameplay(query, max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=API_KEY)

    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video",
        videoLicense="creativeCommon"
    ).execute()

    videos = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append({"video_id": video_id, "title": title})

    return videos


def download_video(video_id, output_path="gameplay.mp4"):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded video: {output_path}")
        return output_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None


def trim_video(input_path, output_path, duration=180):
    try:
        video_clip = VideoFileClip(input_path)
        trimmed_clip = video_clip.subclip(0, min(duration, video_clip.duration))
        trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Trimmed video saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred while trimming the video: {e}")


def grabvideo():
    query = "gameplay footage"
    print("Searching for Creative Commons gameplay footage...")
    videos = search_creative_commons_gameplay(query, max_results=3)

    if videos:
        print("Found the following Creative Commons videos:")
        for idx, video in enumerate(videos, start=1):
            print(
                f"{idx}. {video['title']} "
                f"(https://www.youtube.com/watch?v={video['video_id']})"
            )

        choice = int(input(f"Enter the number of the video to download (1-{len(videos)}): "))
        if 1 <= choice <= len(videos):
            selected_video = videos[choice - 1]
            print(f"Downloading: {selected_video['title']}")
            gameplay_video_path = download_video(selected_video["video_id"])
            gameplay_video_path = "gameplay.mp4" 
            if gameplay_video_path:
                print(f"Gameplay video saved as {gameplay_video_path}.")

                trimmed_video_path = "shortgameplay.mp4"
                trim_video(gameplay_video_path, trimmed_video_path)
            else:
                print("Video download failed.")
        else:
            print("Invalid choice.")
    else:
        print("No Creative Commons videos found.")
