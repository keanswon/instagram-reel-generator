import os
import whisper
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

openai_key = os.environ.get("openai_key")

AUDIO_PATH = os.path.join("audio_files", "askreddit_post_audio.mp3")
TEST_PATH = os.path.join("test_audio", "test.mp3")

OPENAI_API_KEY = openai_key

AUDIO_FOLDER = "audio_files"
subreddit = 'askreddit'

comment_path = os.path.join(AUDIO_FOLDER, f"{subreddit}_comment.mp3")

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )

    return group_into_phrases(transcription.words)

def group_into_phrases(words_with_timestamps, max_words=7, pause_threshold=0.35, buffer=.37):
    phrases = []
    current_phrase = []
    phrase_start = None
    last_end = 0

    for word_data in words_with_timestamps:
        word = word_data.word
        start = word_data.start
        end = word_data.end

        # only start a new phrase if current phrase is empty
        if not current_phrase:
            phrase_start = start

        if start - last_end > pause_threshold and current_phrase:
            phrases.append({
                "phrase": " ".join(current_phrase),
                "start": phrase_start,
                "end": last_end
            })
            current_phrase = []
            phrase_start = start

        current_phrase.append(word)
        last_end = end

        # phrase ends when it meets max words, punctuation, or end of input
        if (
            len(current_phrase) == max_words
            or word_data == words_with_timestamps[-1]
        ):
            phrases.append({
                "phrase": " ".join(current_phrase),
                "start": phrase_start,
                "end": end + buffer # buffer becuase otherwise it's a bit too fast
            })
            current_phrase = []

    return phrases
