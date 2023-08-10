import os
from pathlib import Path
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = os.path.join(BASE_DIR, '.env')
Env.read_env(CONFIG_PATH)
env = Env()
if env is not None:
    is_production_server = env('IS_PRODUCTION_SERVER')
    if is_production_server == 'True':
        from .prod import *
    else:
        from .dev import *
else:
    raise FileNotFoundError("Env File Does not exist")
