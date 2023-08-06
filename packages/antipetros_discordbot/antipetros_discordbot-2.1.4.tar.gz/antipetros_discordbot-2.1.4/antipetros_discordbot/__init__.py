"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = '2.1.4'

import os
from importlib.metadata import metadata
from dotenv import load_dotenv
from psutil import virtual_memory
from datetime import datetime, timedelta, timezone
import logging
MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(MAIN_DIR) is True:

    MAIN_DIR = os.readlink(MAIN_DIR).replace('\\\\?\\', '')

START_TIME = datetime.now(tz=timezone.utc)


def set_env():
    """
    Sets some enviroment variables to be available everywhere.
    Checks if it is being launched from the development environment or not and set the env variable 'IS_DEV' and `PYTHONASYNCIODEBUG` accordingly.

    """
    old_cd = os.getcwd()
    os.chdir(MAIN_DIR)

    os.environ['LOG_CONFIG_RETRIEVE'] = '0'
    os.environ['PYTHONASYNCIODEBUG'] = "1"
    os.environ['ANTIPETRO_START_TIME'] = START_TIME.isoformat()
    os.environ['APP_NAME'] = metadata(__name__).get('name')
    os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')
    os.environ['ANTIPETROS_VERSION'] = metadata(__name__).get('version')
    os.environ['BASE_FOLDER'] = MAIN_DIR
    os.environ['LOG_FOLDER'] = MAIN_DIR
    os.chdir(old_cd)
    os.environ['DISABLE_IMPORT_LOGCALLS'] = "1"
    os.environ['DISABLE_INITIATION_LOG_CALLS'] = "1"
    # os.environ['ANTIPETROS_PROFILING'] = '0'
    _mem_item = virtual_memory()
    memory_in_use = _mem_item.total - _mem_item.available
    os.environ['INITIAL_MEMORY_USAGE'] = str(memory_in_use)
    # os.environ['BOT_CREATOR_NAME'] = "Giddi"
    os.environ['BOT_CREATOR_ID'] = "576522029470056450"
    os.environ['REPO_BASE_URL'] = "https://github.com/official-antistasi-community/Antipetros_Discord_Bot/blob/development"
    os.environ['WIKI_BASE_URL'] = "https://github.com/official-antistasi-community/Antipetros_Discord_Bot/wiki"
    if os.getenv('IS_DEV', 'false').casefold() == 'true':
        os.environ['ALWAYS_CHECK_RATE_LIMITED'] = '1'


set_env()
os.environ['COLLECT_ATTACHMENT_TYPES_ENABLED'] = "0"
