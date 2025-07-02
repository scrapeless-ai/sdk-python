from enum import Enum
import os
from .utils import Logger
from dotenv import load_dotenv

load_dotenv()
log = Logger().with_prefix('Environment')

"""
Scrapeless Actor environment variables

This module provides access to environment variables used by the Scrapeless
Actor runtime. It defines all supported environment variables and provides
utility functions to retrieve them.
"""
class ActorEnv(str, Enum):
    # Environment variables used by Scrapeless api client
    SCRAPELESS_BASE_API_URL = 'SCRAPELESS_BASE_API_URL'
    SCRAPELESS_ACTOR_API_URL = 'SCRAPELESS_ACTOR_API_URL'
    SCRAPELESS_STORAGE_API_URL = 'SCRAPELESS_STORAGE_API_URL'
    SCRAPELESS_BROWSER_API_URL = 'SCRAPELESS_BROWSER_API_URL'
    SCRAPELESS_CRAWL_API_URL = 'SCRAPELESS_CRAWL_API_URL'
    SCRAPELESS_API_KEY = 'SCRAPELESS_API_KEY'
    SCRAPELESS_TEAM_ID = 'SCRAPELESS_TEAM_ID'
    # Environment variables used by Scrapeless Actor runtime
    SCRAPELESS_ACTOR_ID = 'SCRAPELESS_ACTOR_ID'
    SCRAPELESS_RUN_ID = 'SCRAPELESS_RUN_ID'
    SCRAPELESS_INPUT = 'SCRAPELESS_INPUT'
    # Environment variables used by Scrapeless storage services
    SCRAPELESS_DATASET_ID = 'SCRAPELESS_DATASET_ID'
    SCRAPELESS_KV_NAMESPACE_ID = 'SCRAPELESS_KV_NAMESPACE_ID'
    SCRAPELESS_BUCKET_ID = 'SCRAPELESS_BUCKET_ID'
    SCRAPELESS_QUEUE_ID = 'SCRAPELESS_QUEUE_ID'

def get_env(key: str) -> str:
    env = os.getenv(ActorEnv[key].value)
    if env is None:
        raise RuntimeError(f"Environment variable {key} is not defined")
    return env

def get_env_with_default(key: str, default_value: str) -> str:
    env = os.getenv(ActorEnv[key].value)
    return env if env is not None else default_value

def print_env():
    for key in ActorEnv:
        value = os.getenv(key.value)
        log.trace(f"{key}: {value}") 