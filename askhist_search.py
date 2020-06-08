import plac
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


def build_searchstring(mandatory, optional):
    search_string = "({})"
    necessary = " AND ".join(mandatory)
    if optional is not None:
        search_string += " AND ({})"
        options = " OR ".join(optional)
        return search_string.format(necessary, options)
    return search_string.format(necessary)


def search_with(askhistorians: Subreddit, targets, optional=None, n=10):
    """Search for posts containing all of the keywords in target,
    and at least one of the keywords in optional

    Returns a generator of permalinks to answers"""

    search_string = build_searchstring(targets, optional)

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


@plac.annotations(
    mandatory=("Keywords which a post must have", "positional", None, str.split),
    optional=("Keywords which a post must have at least one of", "option", "p", str.split),
    n=("The number of results to search", "option", "n", int))
def main(mandatory, optional, n):
    reddit = praw.Reddit("askhist-search")
    results = search_with(reddit.subreddit("askhistorians"),
                          mandatory, optional=optional, n=n)
    for link in results:
        print(link)


if __name__ == '__main__':
    plac.call(main)
