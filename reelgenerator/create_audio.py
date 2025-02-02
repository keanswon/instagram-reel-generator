import os
import edge_tts
import pandas as pd
import asyncio

VOICE = "en-US-ChristopherNeural"
AUDIO_FOLDER = "audio_files"
VIDEO_RATE = "+57%"

async def generate_post_audio(post_title, comment, subreddit):

    # Combine title and comment with a pause
    text_to_speak = f"{post_title}... {comment}"
    # Generate and save audio
    
    tts = edge_tts.Communicate(text_to_speak, VOICE, rate=VIDEO_RATE)
    await tts.save(os.path.join(AUDIO_FOLDER, f"{subreddit}_post_audio.mp3"))

async def generate_title_audio(post_title, subreddit):
    tts_title = edge_tts.Communicate(post_title, VOICE, rate=VIDEO_RATE)
    title_path = os.path.join(AUDIO_FOLDER, f"{subreddit}_title.mp3")
    await tts_title.save(title_path)

async def generate_comment_audio(comment, subreddit):
    tts_comment = edge_tts.Communicate(comment, VOICE, rate=VIDEO_RATE)
    comment_path = os.path.join(AUDIO_FOLDER, f"{subreddit}_comment.mp3")
    await tts_comment.save(comment_path)

    

# move this to a separate function that can be called
if __name__ == "__main__":
    # Load data from the CSV file
    csv_path = "posts/askreddit_top_post.csv"
    audio_folder = "audio_files"

    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        exit()

    # Read the CSV
    data = pd.read_csv(csv_path)

    # Extract title and comment
    post_title = data.iloc[0]["content"]
    comment = data.iloc[0]["top_comment"]

    # Ensure the audio folder exists
    os.makedirs(audio_folder, exist_ok=True)

    # Generate audio file path
    audio_file_path = os.path.join(audio_folder, "askreddit_post_audio.mp3")

    # Generate audio
    asyncio.run(generate_post_audio(post_title, comment, audio_file_path))
