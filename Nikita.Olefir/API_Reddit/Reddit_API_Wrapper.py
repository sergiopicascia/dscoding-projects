import praw
from API_Reddit.credentials import USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent="MyAPI/1 by (nikitaolefir)",
    )