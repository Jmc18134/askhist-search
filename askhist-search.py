import sys

import praw
from praw.models import Subreddit


MODS = ["Bernardito",
        "Daeres",
        "lngwstksgk",
        "AutoModerator",
        "Celebreth",
        "Georgy_K_Zhukov",
        "Searocksandtrees",
        "jschooltiger",
        "Elm11",
        "sunagainstgold"]


def search_with(askhistorians: Subreddit, targets, optional=None, n=10):
    """Search for posts containing all of the keywords in target,
    and at least one of the keywords in optional

    Returns a generator of permalinks to answers"""
    search_string = "({})"
    necessary = " AND ".join(targets)
    format_string = necessary
    if optional is not None:
        search_string += " AND ({})"
        options = " OR ".join(optional)
        format_string = necessary, options
    search_string = search_string.format(format_string)

    # 'Answered' r/askhistorians posts are defined as those with
    # at least one top-level comment that isn't made by a moderator
    links = []
    posts = askhistorians.search(search_string, limit=n)
    for post in posts:
        if post.num_comments > 1 and any(comment.author is not None
                                         and comment.author.name not in MODS
                                         for comment in post.comments):
            links.append(post.shortlink)
    return links


def main():
    reddit = praw.Reddit("askhist-search")
    res = search_with(reddit.subreddit("askhistorians"), ["mesopotamia"], n=12)
    for p in res:
        print(p)


if __name__ == '__main__':
    main()
