import os

from dotenv import load_dotenv

load_dotenv()


class Logger:
    def __init__(self):
        pass

    def debug(self, message: str) -> None:
        if self.is_verbose():
            print("[DEBUG]{}".format(self.clean_message(message)))

    def info(self, message: str) -> None:
        if self.is_verbose():
            print("[INFO]{}".format(self.clean_message(message)))

    def warning(self, message: str) -> None:
        print("[WARNING]{}".format(self.clean_message(message)))

    def error(self, message: str) -> None:
        print("[ERROR]{}".format(self.clean_message(message)))

    def critical(self, message: str) -> None:
        print("[CRITICAL]{}".format(self.clean_message(message)))

    def is_verbose(self) -> bool:
        if os.getenv("DEBUG") is not None:
            return True

        return False

    def increase_verbosity(self):
        self.lowLogVerbosity = []

    def clean_message(self, message: str) -> str:
        return message


LOG = Logger()
