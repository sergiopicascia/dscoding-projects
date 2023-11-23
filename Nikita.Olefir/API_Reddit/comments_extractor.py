"""
This module contains a function to extract comments from a thread in a subreddit.
"""
from API_Reddit.Reddit_API_Wrapper import reddit
import pandas as pd


def comments_extractor(subreddit_name: str, submission_id: str):
    """This function collects all the comments from a Reddit threard.


    Arguments:
        subreddit_name (str): the name of the subreddit where thread is located
        submission_id (str): the ID of the thread

    Returns:
        pd.DataFrame: dataframe with the following columns:
        1) 'author': author of the comment
        2) 'body': the text of comment
        3) 'score': the score of the comments
        4) 'created_utc': time the comment was created

    Examples:
        comments_extractor('Python','17x1kec')
    """

    subreddit_name = subreddit_name
    submission_id = submission_id
    submission = reddit.submission(id=submission_id)
    all_comments = []
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        all_comments.append(
            {
                "author": comment.author.name if comment.author else "[deleted]",
                "body": comment.body,
                "created_utc": comment.created_utc,
            }
        )
    return pd.DataFrame(all_comments)
