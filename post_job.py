from loguru import logger
from redis import Redis
from typing import List, Optional
from utils import load_config


def post_to_twitter(twitter_api, message: str):
    # https://medium.com/@divyeshardeshana/how-to-post-tweet-using-python-b7af66013419
    # https://projects.raspberrypi.org/en/projects/getting-started-with-the-twitter-api/5
    # https://github.com/sns-sdks/python-twitter
    print(message)


def fetch_message(queue_conn, queue_key: str) -> Optional[str]:
    message = queue_conn.lpop(queue_key)
    if message:
        return message.decode('utf-8')


def main():
    logger.debug('Initialize APIs')
    twitter_client = None
    config = load_config()
    redis_client = Redis()

    logger.debug('Fetch message from queue')
    message = fetch_message(redis_client, config['storage']['queue_key'])
    if message:
        logger.debug('Post to twitter')
        post_to_twitter(twitter_client, message)
        return
    logger.warning('Queue is empty')


if __name__ == '__main__':
    main()
