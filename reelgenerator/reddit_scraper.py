import praw
import os
import pandas as pd
import requests

from dotenv import load_dotenv

reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")

post_id = None

seen_posts = []

reddit = praw.Reddit(client_id=reddit_client_id,
                    client_secret=reddit_client_secret,
                    user_agent='reddit scraper by sean')

def get_top_post(sub):
    subreddit = reddit.subreddit(sub)
    top_posts = subreddit.hot(limit=5)

    for post in top_posts:
        if post.id not in seen_posts:
            top_post = post
            seen_posts.append(post.id)
            break
    
    return {
        "url": top_post.url,
        "content": top_post.title,
        "post_id": top_post.id
    }


def get_top_comment(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        word_count = len(comment.body.split())
        if 40 <= word_count <= 100:
            # clean up string before returning - reddit bolds / italicizes with asterisks
            return comment.body.replace("*","").strip()
    return "No suitable comment found."

def save_to_csv(data, file_path):
    os.makedirs("posts", exist_ok=True)
    df = pd.DataFrame([data])
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def get_post(sub, filepath):
    post = get_top_post(sub)
    post["top_comment"] = get_top_comment(post["post_id"])
    save_to_csv(post, filepath)