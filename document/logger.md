## logger.py - 日志管理模块

本模块提供统一的日志管理功能，用于全项目日志记录和输出，支持：

1. **多格式输出**：彩色终端输出、结构化 JSON 输出。
2. **多级日志管理**：可针对不同模块生成独立日志文件，同时支持全局错误日志。
3. **灵活配置**：日志级别、输出路径、是否彩色显示均可自定义。
4. **简易调用**：通过 `get_logger()` 获取已有 logger，若未初始化则自动生成默认配置。[^awful_1]

---

#### 函数和类说明

### class ColorFormatter

    继承 logging.Formatter

#### def format

将日志记录格式转换为彩色文本输出。

    彩色输出规则：
        - DEBUG   → 青色
        - INFO    → 绿色
        - WARNING → 黄色
        - ERROR   → 红色
        - CRITICAL→ 紫色

    格式示例：
        [2025-11-01 22:30:15.123] [INFO] 日志内容

    Args:
        record (logging.LogRecord): 待格式化的日志记录对象。

    Returns:
        str: 带时间戳、日志等级和颜色的字符串，用于终端输出。

---

### class JSONFormatter

    继承 loggging.Formatter

#### def format

将日志数据加工为 JSON 字符串:

时间 + 日志等级 + 日志内容 + 模块名 + 日志所在函数名 + 行号

    Args:
        record (logging.LogRecord): 待格式化的日志记录对象。

    Returns:
        JSON: 带时间戳、日志等级、内容、模块名、日志所在函数名和行号的 JSON 字符串

---

### def init_logger

通过默认配置对 logger 进行初始化，添加三个 handler 分别用于打印、正常日志存储和报错日志存储[^awful_2]。

    Args:
        level (int, optional):日志级别，默认 logging.DEBUG。
        use_color (bool, optional): 是否使用彩色输出，默认 True。
        output_json (bool, optional): 是否使用 JSON 格式输出日志，默认 False。
        log_path (Optional[str], optional): 日志文件路径，默认 None。
        name (Optional[str], optional): logger 名称，默认 None。

    Returns:
        logging.Logger: 一个初始化好的 logger 对象。

### def get_logger

获取已有 logger, 如果未初始化则提供默认配置。

理想情况下这会是外部模块统一调用的接口[^awful_1]。

    Args:
        name (Optional[str]): logger 的名称，默认 None。
        log_path (Optional[str]): 日志存储路径，默认 None。

    Returns:
        logging.Logger: 一个初始化好的 logger 对象。

[^awful_1]: 当前版本下 main.py 使用 init_logger() 获取 logger 对象而不是统一经过这一函数，在后续版本会优化代码。
[^awful_2]: 我知道这样不好但反正能用先发上来再说如果有时间会进行优化的红豆泥私密马赛。
