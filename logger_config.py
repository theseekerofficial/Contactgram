import sys
import pytz
from loguru import logger
from datetime import datetime
from utils.processor.load_env import env_dict

def configure_logger():
    logger.remove()

    custom_timezone = pytz.timezone(env_dict.get("TIMEZONE", "UTC"))

    def set_datetime(record):
        record["extra"]["datetime"] = datetime.now(custom_timezone).strftime("%Y-%m-%d %H:%M:%S")

    logger.configure(patcher=set_datetime)

    logger.add(
        sys.stderr,
        level="INFO",
        format="<magenta>{extra[datetime]}</magenta> | "
               "<level>{level: <8}</level> | "
               "<yellow>{name}</yellow>:<cyan>{function}</cyan> | "
               "<green>{message}</green>",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        "logs/{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="00:00",
        retention="7 days",
        compression="zip",
        format="<magenta>{extra[datetime]}</magenta> | "
               "<level>{level: <8}</level> | "
               "<yellow>{name}</yellow>:<cyan>{function}</cyan> | "
               "<green>{message}</green>",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
