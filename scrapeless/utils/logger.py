import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

# Log level definitions
class LogLevel:
    TRACE = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARNING
    ERROR = logging.ERROR

# Add TRACE level to logging
logging.addLevelName(LogLevel.TRACE, 'TRACE')

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.TRACE):
        self._log(LogLevel.TRACE, message, args, **kwargs)
logging.Logger.trace = trace

# Color configuration for console output
LEVEL_COLORS = {
    LogLevel.TRACE: '\033[90m',   # gray
    LogLevel.DEBUG: '\033[36m',   # cyan
    LogLevel.INFO: '\033[32m',    # green
    LogLevel.WARN: '\033[33m',    # yellow
    LogLevel.ERROR: '\033[31m',   # red
}
RESET_COLOR = '\033[0m'

# Prefix color configuration
PREFIX_COLORS = ['\033[36m', '\033[35m', '\033[34m', '\033[33m', '\033[32m']

def colorize(text: str, color: str) -> str:
    return f"{color}{text}{RESET_COLOR}"

def colorize_prefix(prefix: str) -> str:
    if not prefix:
        return ''
    hash_val = sum(ord(c) for c in prefix)
    color = PREFIX_COLORS[hash_val % len(PREFIX_COLORS)]
    return colorize(prefix, color)

# Get log directory
LOG_ROOT_DIR = os.environ.get('SCRAPELESS_LOG_ROOT_DIR', './logs')
os.makedirs(LOG_ROOT_DIR, exist_ok=True)

# Logger factory
class Logger:
    def __init__(self, prefix: Optional[str] = None):
        self.prefix = prefix or ''
        self.logger = logging.getLogger(prefix or 'scrapeless')
        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(self._get_console_formatter())
            self.logger.addHandler(ch)
            # File handler
            fh = TimedRotatingFileHandler(
                os.path.join(LOG_ROOT_DIR, 'scrapeless.log'),
                when='midnight',
                backupCount=int(os.environ.get('SCRAPELESS_LOG_MAX_BACKUPS', 5))
            )
            fh.setLevel(logging.INFO)
            fh.setFormatter(self._get_file_formatter())
            self.logger.addHandler(fh)
        self.logger.setLevel(logging.INFO)

    def _get_console_formatter(self):
        class ConsoleFormatter(logging.Formatter):
            def format(inner_self, record):
                level_color = LEVEL_COLORS.get(record.levelno, '')
                prefix_str = colorize_prefix(self.prefix) + ': ' if self.prefix else ''
                msg = super(ConsoleFormatter, inner_self).format(record)
                return f"{level_color}{record.levelname}{RESET_COLOR} {prefix_str}{msg}"
        return ConsoleFormatter('%(message)s')

    def _get_file_formatter(self):
        return logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%dT%H:%M:%SZ')

    def trace(self, msg, *args, **kwargs):
        self.logger.trace(msg, *args, **kwargs)
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
    def warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
    def with_prefix(self, prefix: str):
        return Logger(prefix)

# Export a default logger instance
logger = Logger() 