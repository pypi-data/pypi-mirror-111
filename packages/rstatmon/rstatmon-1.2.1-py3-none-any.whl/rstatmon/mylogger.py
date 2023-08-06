import tarfile
from pathlib import Path
from datetime import datetime
from loguru import logger


class MyLogger():
    """Logging class with loguru module.
    """

    def __init__(self):
        self.root = Path(__file__).resolve().parent / "data/log"

    def logger_setup(self):
        data_root = Path(__file__).resolve().parent / "data/log"
        today = datetime.now().strftime("%Y%m")
        data_file = "{}.log".format(datetime.now().strftime("%Y%m%d"))
        data_dir = data_root / today
        dst = data_dir / data_file
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.add(dst, format="[{level} {time:YYYY-MM-dd HH:mm:ss:SSS}] {message}")

    def get_log_dst(self):
        """Determines the file to write log to.

        The format of the filename is   The log file is stored in the 'data/log' directory.

        """
        data_root = Path(__file__).resolve().parent / "data/log"
        today = datetime.now().strftime("%Y%m")
        data_file = "{}.log".format(datetime.now().strftime("%Y%m%d"))
        data_dir = data_root / today
        data_dir.mkdir(parents=True, exist_ok=True)
        dst = data_dir / data_file
        logger.remove()
        logger.add(str(dst), format="[{level} {time:YYYY-MM-DD HH:mm:ss:SSS}] {message}")

    def write_log(self, msg: str, level: str):
        """Writes a message to log file.

        The message is written to the file determined in the 'get_log_dst`. The
        logging level shows the importtance of the message and is classfied by
        as follows.

            - info : Information
            - success: Operation success such as login and logout
            - error: Operation failure such as login and logout

        Args:
            msg (str)): A message to write
            level (str): Logging level
        """
        self.get_log_dst()
        if level == "info":
            logger.info(msg)
        elif level == "success":
            logger.success(msg)
        elif level == "error":
            logger.error(msg)
        elif level == "warning":
            logger.warning(msg)

    def log_compress(self):
        """Compress log file to tar.gz
        """
        logs = [i for i in self.root.glob("**/*") if i.is_file()]
        for log in logs:
            # compress
            tar = f"{str(log)}.tar.gz"
            with tarfile.open(tar, "w:gz") as f:
                f.add(str(log))

