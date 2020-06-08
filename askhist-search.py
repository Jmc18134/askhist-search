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
    if optional is not None:
        search_string += " AND ({})"
        options = " OR ".join(optional)
        search_string = search_string.format(necessary, options)
    else:
        search_string = search_string.format(necessary)

    # 'Answered' r/askhistorians posts are defined as those with
    # at least one top-level comment that isn't made by a moderator
    answered = (post for post in askhistorians.search(search_string, limit=n)
                if post.num_comments > 1 and
                any(comment.author is not None
                    and comment.author.name not in MODS
                    for comment in post.comments))

    return (answer.permalink for answer in answered)


def main():
    reddit = praw.Reddit("askhist-search")
    search_with(reddit.subreddit("askhistorians"), ["mesopotamia"], n=12)


if __name__ == '__main__':
    main()
