##if execution happen, logg all information in doc file that we can track error
import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now(.strftime('%m_%d_%Y-%H_%M_%S'))}.log"
logs_path=os.path.join(os.getcwd(),"log", LOG_FILE)
os.makedirs(logs_path, exist_ok=true)

LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE)

def setup_logging(log_filename="app.log"):
    logging.basicConfig(
        filename=LOG_FILE_PATH
        level=logging.INFO, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format of the log

    )

setup_logging("myapp.log")