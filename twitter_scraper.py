import snscrape.modules.twitter as sntwitter

def search_tweets(candiates):
    search_query = candiates
    search_results = list(sntwitter.TwitterSearchScraper(search_query).get_items())
    profile_urls = [tweet.user.url for tweet in search_results]
    return profile_urls



