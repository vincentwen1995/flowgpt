import praw
from utils.dynaconf_utils import settings

CLIENT_ID = settings.REDDIT_PERSONAL_USE_SCRIPT
CLIENT_SECRET = settings.REDDIT_PERSONAL_USE_SECRET
USERNAME = settings.REDDIT_USERNAME
VERSION = "0.1.0"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=f"linux:flowgpt:v{VERSION} (by /u/{USERNAME})",
)


def get_popular_posts(subreddit_name: str, n: int = 3):
    """
    Get popular posts from a subreddit.

    Args:
        subreddit_name (str): Name of the subreddit to retrieve posts from.
        n (int, optional): Number of posts to retrieve. Defaults to 10.

    Returns:
        list: A list of dictionaries representing the popular posts.
    """
    subreddit = reddit.subreddit(subreddit_name)
    popular_posts = subreddit.hot(limit=n)

    return [
        {
            "score": post.__dict__["score"],
            "ups": post.__dict__["ups"],
            "title": post.__dict__["title"],
            "selftext": post.__dict__["selftext"],
        }
        for post in popular_posts
    ]


def fetch_posts():
    subreddits = settings.REDDIT_SUBREDDITS
    results = {}
    for subreddit in subreddits:
        try:
            results.update({subreddit: get_popular_posts(subreddit)})
        except Exception as e:
            print(f"Failed fetching posts for subreddit: {subreddit}")
            print(e)
            continue
    # return {subreddit: get_popular_posts(subreddit) for subreddit in subreddits}
    return results
