# gets screenshot from screenshots.py

import os
import pandas as pd
import random
import PIL
from PIL import Image
import asyncio

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, ColorClip, concatenate_videoclips

from screenshots import get_title_screenshot
from reddit_scraper import get_post
from create_audio import generate_post_audio, generate_comment_audio, generate_title_audio
from transcription import transcribe_audio

SCREENSHOT_PATH = "screenshots"
VIDEO_FOLDER = "video_files"
AUDIO_FOLDER = "audio_files"
SHORTS_FOLDER = "shorts"
DATA_FOLDER = "posts"
CAPTION_FOLDER = "textclip"

subreddit = "AskReddit"

async def main():
    """
    RETRIEVING POST DATA
    """

    # scrape reddit
    file_path = os.path.join(DATA_FOLDER, f"{subreddit}_data.csv")
    get_post(subreddit, file_path)

    # laod data
    csv_path = f"posts/{subreddit}_data.csv"

    df = pd.read_csv(csv_path)

    # read post title and comment to create audio file
    post_title = df.at[0, "content"]
    comment = df.at[0, "top_comment"]

    """
    MAKING AUDIO FILE
    """

    # generate audio
    await asyncio.gather(
        generate_post_audio(post_title, comment, subreddit.lower()),
        generate_title_audio(post_title, subreddit.lower()),
        generate_comment_audio(comment, subreddit.lower())
    )

    """
    GETTING TITLE SCREENSHOT // SET DURATION
    """

    post_url = df.at[0, "url"]
    post_id = df.at[0, "post_id"]

    title_path = os.path.join(SCREENSHOT_PATH, f"{post_id}.png")

    # retrieve screenshot
    get_title_screenshot(post_url, post_id, title_path)

    """
    COMBINING VIDEOS / EXPORTING VIDEO
    """
    # make the path to the background footage - minecraft parkour!
    out_path = os.path.join(VIDEO_FOLDER, "parkour_cropped.mp4")
    shorts_path = os.path.join(SHORTS_FOLDER, "short.mp4")
    subtitle_path = os.path.join(CAPTION_FOLDER, f"{post_id}.mp4")

    make_movie(out_path, AUDIO_FOLDER, title_path, shorts_path)

def make_movie(video_path, audio_folder, screenshot_path, output_path):
    # Load the video and audio
    final_audio_path = os.path.join(audio_folder, f"{subreddit.lower()}_post_audio.mp3")
    title_audio_path = os.path.join(audio_folder, f"{subreddit.lower()}_title.mp3")
    comment_audio_path = os.path.join(audio_folder, f"{subreddit.lower()}_comment.mp3")

    video = VideoFileClip(video_path)
    title_audio = AudioFileClip(title_audio_path)
    comment_audio = AudioFileClip(comment_audio_path)
    final_audio = AudioFileClip(final_audio_path)

    # Match video snippet duration to audio length
    audio_duration = title_audio.duration + comment_audio.duration
    video_duration = video.duration

    # Choose a random start time for the video snippet
    start_time = random.uniform(0, video_duration - audio_duration)

    video_snippet = video.subclip(start_time, start_time + audio_duration)

    # edit the duration - make it the title's duration
    os.makedirs(SCREENSHOT_PATH, exist_ok=True)

    screenshot = ImageClip(screenshot_path).set_duration(title_audio.duration).set_position("center")
    new_width = int(video_snippet.size[0] * .9)
    aspect_ratio = screenshot.size[1] / screenshot.size[0]
    new_height = int(new_width * aspect_ratio)

    screenshot = screenshot.resize(width=new_width, height=new_height)

    # make subtitle clip
    transcription = transcribe_audio(comment_audio_path)
    subtitle_clip = create_subtitle_clip(transcription)

    screenshot_full_frame = CompositeVideoClip(
        [screenshot.set_position("center")], 
        size=video_snippet.size
    ).set_duration(title_audio.duration)

    overlay_clip = concatenate_videoclips([screenshot_full_frame, subtitle_clip])

    overlaid_video = CompositeVideoClip([video_snippet, overlay_clip])
    

    # Add the audio to the video
    final_video = overlaid_video.set_audio(final_audio)

    # Save the output
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# change aspect ratio of video
def convert_to_short_format(input_path, out_path):
    # Load the video
    video = VideoFileClip(input_path)

    # Calculate crop dimensions for 9:16
    width, height = video.size
    target_aspect_ratio = 9 / 16

    if width / height > target_aspect_ratio:
        # Crop horizontally
        new_width = int(height * target_aspect_ratio)
        crop_x = (width - new_width) // 2
        cropped_video = video.crop(x1=crop_x, x2=crop_x + new_width)
    else:
        # Crop vertically
        new_height = int(width / target_aspect_ratio)
        crop_y = (height - new_height) // 2
        cropped_video = video.crop(y1=crop_y, y2=crop_y + new_height)

    # Resize to ensure it's exactly 9:16
    resized_video = cropped_video.resize(height=1920)  # Resize to full HD height

    # override video
    resized_video.write_videofile(out_path, codec="libx264", audio_codec="aac")

# function to create a subtitle clip
def create_subtitle_clip(transcription):
    clips = []
    video_size = (1080, 1920)
    
    for phrase in transcription:
        start_time = phrase['start']
        end_time = phrase['end']
        text = phrase['phrase']

        duration = end_time - start_time

        text_clip = (
            TextClip(
            txt=text,
            fontsize=50,
            color="white",
            font="Arial",
            size=video_size,
            )
            .set_duration(duration)
        )

        text_clip = text_clip.set_position(("center", "center"))

        # Overlay text on top of the border

        clips.append(text_clip)

    combined_clip = concatenate_videoclips(clips)

    return combined_clip





if __name__ == "__main__":
    asyncio.run(main())