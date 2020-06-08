import sys

import plac
import praw
from praw.models import Subreddit


# r/askhistorians mod list
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


def get_redirect(comment):
    return None


def build_searchstring(mandatory, optional):
    """Take in two lists of keywords and output a reddit-search string
    Mandatory keywords are those which must all occur in the post,
    whereas only one of the optional keywords must appear"""

    # I hate how this looks, but I don't see a much better way of doing it
    # DRY is going to get violated no matter what you do
    mandatory_words = "({})"
    if mandatory is not None:
        mandatory_words = mandatory_words.format(" AND ".join(mandatory))
    optional_words = "({})"
    if optional is not None:
        optional_words = optional_words.format(" OR ".join(optional))
        if mandatory is not None:
            return "{} AND {}".format(mandatory_words, optional_words)
        return optional_words
    return mandatory_words


def search_with(askhistorians: Subreddit, targets, optional=None, n=10):
    """Search for posts containing all of the keywords in target,
    and at least one of the keywords in optional

    Returns a generator of permalinks to answers"""

    search_string = build_searchstring(targets, optional)

    links = []
    # r/askhistorians posts always have an automod comment first
    posts = (p for p in askhistorians.search(search_string, limit=n) if p.num_comments > 1)
    for post in posts:
        # 'Answered' r/askhistorians posts are defined as those with
        # at least one top-level comment that isn't made by a moderator
        answers = (comment for comment in post.comments if comment.author
                   is not None and comment.author.name not in MODS)

        # We only need one answer per post, so just get the first one
        first = next(answers, None)
        if first is None:
            continue

        nested_links = get_redirect(first)
        if nested_links is not None:
            links += (nested_links)
        else:
            links.append(post.shortlink)

    return links


@plac.annotations(
    mandatory=("Keywords which a post must have", "option", "m", str.split),
    optional=("Keywords which a post must have at least one of", "option", "p", str.split),
    n=("The number of results to search", "option", "n", int),
    r=("The max number of results to display", "option", "r", int))
def main(mandatory, optional, n, r):
    if mandatory is None and optional is None:
        sys.stderr.write("{}: At least one keyword (optional or mandatory) is required\n".format(sys.argv[0]))
        sys.exit(1)
    reddit = praw.Reddit("askhist-search")
    results = search_with(reddit.subreddit("askhistorians"),
                          mandatory, optional=optional, n=n)
    for link in results[:r]:
        print(link)


if __name__ == '__main__':
    plac.call(main)
