import os
from dotenv import dotenv_values


APP_CONFIG = {
    **dotenv_values(".env"),
    **os.environ,  # override loaded values with environment variables
}
