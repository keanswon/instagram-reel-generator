# Auto Youtube Shorts Creator

## Overview

I created this script to automatically create and upload short-form content to a fresh youtube channel.

The program scrapes a top post and comment from r/AskReddit. The content is read out using edge-tts, and
captions are generated using OpenAI's whisper model. To jive with the trend of short form content, 
I overlaid a parkour video in the background (file is too large to upload to github). Finally, the program
uses selenium to automatically upload to youtube. A title and description are automatically generated.

## results:

https://www.youtube.com/@askingredditeveryday - posting here as proof of concept

## Usage

1. pip3 install requirements.txt
2. modify links and filepaths (in the future I will make this part easier)
3. download a cropped parkour video (or manually crop it)
4. python create_movie.py
5. python upload.py

## What I Lerned

Apart from using more specified libraries like reddit.py and moviepy, this project taught me a lot about using pandas, which
I also found use for in my other projects, like my (attempted) trading bot. This project improved my skills on organizing and
manipulating data. Additionally, with the addition of secret keys and such in this project, I went through a long debugging process
to push the code successfully to github.

## Project Structure

| File/Folder         | Description |
|---------------------|-------------|
| `audio_files/`      | Contains TTS files for the voiceover |
| `posts/`            | Contains scraped posts from AskReddit |
| `screenshots/`      | Contains title screenshots - contains examples |
| `shorts/`           | Folder the video will be saved to |
| `video_files/`      | Folder to insert parkour video |
| `create_audio.py`   | Uses edge_tts to create audio for the video |
| `create_video.py`   | Uses moviepy to combine audio, parkour, and captions |
| `reddit_scraper.py` | Scrapes posts from reddit |
| `screenshots.py`    | Takes a screenshot of the title |
| `transcription.py`  | Transcribes the ai audio using whisper |
| `requirements.txt`  | Lists all dependencies needed to run the project. |
| `README.md`         | Documentation for the project. |

## future improvements

1. add a background to the textclip
2. edit hard-coded urls and such so that others can use