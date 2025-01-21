import praw
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, TextClip, concatenate_videoclips
from moviepy.editor import AudioFileClip
from time import sleep

def create_reddit_video():
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='')

    subreddit = reddit.subreddit("confessions")
    hot_posts = subreddit.hot(limit=1)

    for post in hot_posts:
        hot_post = post.title + "\n\n" + post.selftext
        comments = post.comments[:3]  
        comments_text = "\n\n".join([comment.body for comment in comments])

    with open("redditconfessions.txt", "w") as file:
        file.write(f"\n{hot_post}\n\n\n{comments_text}")

    narration_text = hot_post + "\n\n" + comments_text
    tts = gTTS(narration_text, lang="en")
    tts.save("narration.mp3")

    try:
        video_clip = VideoFileClip("shortgameplay.mp4")
        audio_clip = AudioFileClip("narration.mp3")

        video_clip_resized = video_clip.resize(height=1920)
        video_clip_resized = video_clip_resized.set_fps(24)

        text_overlay = TextClip(hot_post + "\n" + comments_text, fontsize=30, color="white", size=(1080, 1920))
        text_overlay = text_overlay.set_pos('center').set_duration(video_clip_resized.duration)

        final_audio = audio_clip.subclip(0, min(video_clip_resized.duration, audio_clip.duration))
        final_video = video_clip_resized.set_audio(final_audio)

        final_video = concatenate_videoclips([final_video.set_duration(video_clip_resized.duration)])
        final_video = final_video.set_audio(final_audio)

        final_video.write_videofile("reddit_overlay_video.mp4", codec="libx264", audio_codec="aac")

        os.remove("narration.mp3")

        print("Video creation complete.")

    except Exception as e:
        print(f"An error occurred while creating the video: {e}")

