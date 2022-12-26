import yaml
import os
from typing import Optional, Any, Dict
from dataclasses import dataclass
import marshmallow_dataclass


@dataclass
class ChatGPTConfigSchema:
    prompt_template: str


@dataclass
class StorageConfigSchema:
    queue_key: str

@dataclass
class TwitterConfigSchema:
    API_KEY: str
    API_SECRET_KEY: str
    BEARER_TOKEN: str
    ACCESS_KEY: str
    ACCESS_SECRET: str


@dataclass
class ConfigSchema:
    chat_gpt: ChatGPTConfigSchema
    storage: StorageConfigSchema
    twitter: TwitterConfigSchema


config_schema = marshmallow_dataclass.class_schema(ConfigSchema)()


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    config_path = config_path or os.environ.get('CONFIG_PATH', 'config.yaml')
    if not os.path.exists(config_path):
        raise ValueError('Can\'t find config')
    with open(config_path, "r") as f:
        try:
            config_data = yaml.safe_load(f)
            config = config_schema.load(config_data)
            return config_schema.dump(config)
        except yaml.YAMLError:
            raise ValueError(f'Can\'t read config on path {config_path}')


if __name__ == '__main__':
    print(load_config('./configs/cfg.yaml'))
