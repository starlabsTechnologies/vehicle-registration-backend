import logging

# Custom formatter for colorizing log levels
class ColorizedFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
    }

    def format(self, record):
        # Get the color for the log level
        color = self.COLORS.get(record.levelname, '')
        reset = '\033[0m'
        # Format the message
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level_name = f"{color}{record.levelname}{reset}"  # Colorize level name
        message = f"{time} [{level_name}] {record.getMessage()}"
        return message

# Configure logger
logger = logging.getLogger('app_logger')
handler = logging.StreamHandler()
formatter = ColorizedFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)