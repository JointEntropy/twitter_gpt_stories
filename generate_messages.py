from chatgpt_wrapper import ChatGPT
from loguru import logger
from utils import load_config
from redis import Redis
from typing import List


def generate_message(chat_gpt_bot, text_request: str) -> str:
    response = chat_gpt_bot.ask(text_request)
    return response


def save_messages(queue_conn, queue_key: str, messages: List[str]):
    queue_conn.lpush(queue_key, *messages)


def main():
    logger.debug('Initialize APIs')
    config = load_config()
    chat_gpt_bot = ChatGPT()
    redis_client = Redis()

    messages = []
    for seed in range(2):
        logger.debug('Generate message with chatGPT')
        text_request = config['chat_gpt']['prompt_template'].format(seed=seed)
        message = generate_message(chat_gpt_bot, text_request)
        messages.append(message)
    logger.debug('Save messages to storage')
    save_messages(redis_client, config['storage']['queue_key'], messages=messages)


if __name__ == '__main__':
    main()
