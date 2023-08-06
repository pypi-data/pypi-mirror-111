"""
                              $$\ 
                              $$ |
$$$$$$$\   $$$$$$\   $$$$$$\  $$ |  $$\ 
$$  __$$\ $$  __$$\ $$  __$$\ $$ | $$  |
$$ |  $$ |$$ /  $$ |$$ |  \__|$$$$$$  / 
$$ |  $$ |$$ |  $$ |$$ |      $$  _$$<  
$$ |  $$ |\$$$$$$  |$$ |      $$ | \$$\ 
\__|  \__| \______/ \__|      \__|  \__|
"""
from nork.core import paths
from dotenv import load_dotenv
import toml

__version__ = "0.1.14"

load_dotenv()

config = dict()

try:
    config = toml.load(f=f"{paths.PROJECT_PATH}/nork.toml")
except Exception as exception:
    pass
