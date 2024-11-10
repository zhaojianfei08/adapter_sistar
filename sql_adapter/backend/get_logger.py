import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

logger_params = {
    "logger_name": "sync_data_app",
    "total_level": 20,
    "file_handler_level": 10,
    "control_handler_level": 20,
    "file_name": "./sync_data_app.log",
    "mode": "a",
    "max_bytes": 10485760,
    "backup_count": 10,
    "encoding": "UTF-8",
    "format": "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
}


def get_logger(logger_name, total_level, file_name, mode, max_bytes, backup_count, encoding, file_handler_level,
               control_handler_level, format) -> logging.getLogger():
    logger = logging.getLogger(logger_name)
    logger.setLevel(total_level)  # 设置日志级别
    file_handler = ConcurrentRotatingFileHandler(filename=file_name,
                                                 mode=mode,
                                                 maxBytes=max_bytes,
                                                 backupCount=backup_count,
                                                 encoding=encoding)  # 设置输出文件
    file_handler.setLevel(file_handler_level)
    control_handler = logging.StreamHandler()
    control_handler.setLevel(control_handler_level)
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    control_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(control_handler)
    return logger


logger = get_logger(**logger_params)
