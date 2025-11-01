# logger.py
'''
logger模块一共提供
'''

import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 彩色输出可选
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
except ImportError:
    Fore = Style = None  

_err_log_path: Optional[str] = None


class ColorFormatter(logging.Formatter):
    """彩色输出日志"""
    COLORS = {
        logging.DEBUG: Fore.CYAN if Fore else "",
        logging.INFO: Fore.GREEN if Fore else "",
        logging.WARNING: Fore.YELLOW if Fore else "",
        logging.ERROR: Fore.RED if Fore else "",
        logging.CRITICAL: Fore.MAGENTA if Fore else "",
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        将日志记录格式化为一定格式的彩色文本输出。

        Args:
            record (logging.LogRecord): 待格式化的日志记录对象。

        Returns:
            str: 带时间戳、日志等级和颜色的字符串，用于终端输出。
        """
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL if Style else ""
        time_str = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        message = super().format(record)
        return f"[{time_str}] {color}[{record.levelname}] {message}{reset}"


class JSONFormatter(logging.Formatter):
    """结构化 JSON 日志"""
    def format(self, record: logging.LogRecord) -> str:
        '''
        将日志数据加工为一定格式的 JSON 字符串:

        Args:
            record (logging.LogRecord): 待格式化的日志记录对象。

        Returns:
            JSON: 带时间戳、日志等级、内容、模块名、日志所在函数名和行号的 JSON 字符串
        '''
        log_dict = {
            "time": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        if record.args:
            log_dict["args"] = record.args
        return json.dumps(log_dict, ensure_ascii=False)


# ======= 全局接口 =======
def init_err_path(err_log_path: Optional[str] = None):
    # 加载err日志路径
    global _err_log_path
    _err_log_path = err_log_path


def init_logger(level=logging.DEBUG,
                use_color=True,
                output_json=False,
                log_path: Optional[str] = None,  
                name: Optional[str] = None) -> logging.Logger:
    """
    通过默认配置对 logger 进行初始化。

    Args:
        level (int, optional): 日志级别，默认 logging.DEBUG。
        use_color (bool, optional): 是否使用彩色输出，默认 True。
        output_json (bool, optional): 是否使用 JSON 格式输出日志，默认 False。
        log_path (Optional[str], optional): 日志文件路径，默认 None。
        name (Optional[str], optional): logger 名称，默认 None。

    Returns:
        logging.Logger: 一个初始化好的 logger 对象。
    """
    # 获取 logger 对象
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 选择打印格式并添加到一个handler
    if output_json:
        formatter = JSONFormatter()
    elif use_color:
        formatter = ColorFormatter("%(message)s")
    else:
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 添加一个handler用于判断文件名是否用于生成结果
    if log_path:
        log_file = Path(log_path)   

        mode = 'a' if log_file.name in ["main.log", "config.log"] else 'w'
        file_handler = logging.FileHandler(filename=str(log_file), mode=mode, encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # 添加一个handler用于管理全局 ERROR 日志
    if _err_log_path:
        err_handler = logging.FileHandler(_err_log_path, mode="a", encoding="utf-8")
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"))
        logger.addHandler(err_handler)

    return logger


def get_logger(name: Optional[str] = None, log_path: Optional[str] = None) -> logging.Logger:
    """
    获取已有 logger, 如果未初始化则提供默认配置。

    Args:
        name (Optional[str]): logger 的名称，默认 None。
        log_path (Optional[str]): 日志存储路径，默认 None。

    Returns:
        logging.Logger: 一个初始化好的 logger 对象。
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        init_logger(name=name, log_path=log_path)
    return logger

if __name__ == "__main__":
    log = init_logger(level=logging.DEBUG, use_color=True, output_json=False)
    log.debug("调试模式启动")
    log.info("启动 CDN 模块", extra={"submodule": "cdn"})
    log.warning("连接延迟较高")
    log.error("任务失败", exc_info=False)
    log.critical("系统崩溃！")
