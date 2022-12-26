from loguru import logger
from redis import Redis
from typing import List, Optional
from utils import load_config
import tweepy


def post_to_twitter(twitter_api, message: str):
    # https://medium.com/@divyeshardeshana/how-to-post-tweet-using-python-b7af66013419
    # https://projects.raspberrypi.org/en/projects/getting-started-with-the-twitter-api/5
    # https://github.com/sns-sdks/python-twitter
    # https://developer.twitter.com/en/portal/products/elevated
    twitter_api.update_status(message)


def fetch_message(queue_conn, queue_key: str) -> Optional[str]:
    message = queue_conn.lpop(queue_key)
    if message:
        return message.decode('utf-8')


def main():
    logger.debug('Initialize APIs')
    config = load_config()
    auth = tweepy.OAuthHandler(config['twitter']['API_KEY'], config['twitter']['API_SECRET_KEY'])
    auth.set_access_token(config['twitter']['ACCESS_KEY'], config['twitter']['ACCESS_SECRET'])
    twitter_client = tweepy.API(auth)

    redis_client = Redis()

    logger.debug('Fetch message from queue')
    # message = fetch_message(redis_client, config['storage']['queue_key'])
    message = 'Hello world'
    if message:
        logger.debug('Post to twitter')
        post_to_twitter(twitter_client, message)
        return
    logger.warning('Queue is empty')


if __name__ == '__main__':
    main()
