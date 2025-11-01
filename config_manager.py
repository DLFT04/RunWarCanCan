import json
import os
from typing import Any, Dict

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "level": "DEBUG",       # 日志级别
    "use_color": True,      # 是否彩色输出日志
    "output_json": False,   # 是否输出 JSON 格式
    "name": None,           # 可选日志名
    "log":True,             # 是否启用日志输出
    "log_path": "./log",    # 日志输出路径
    "proxy": None,          # 代理设置
    "show_logo": True       # 展示logo
}


def load_config() -> Dict[str, Any]:
    """加载配置文件，如果不存在则创建默认配置"""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: Dict[str, Any]):
    """保存配置到文件"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def update_config(key: str, value: Any):
    """更新单个配置项"""
    config = load_config()

    # 对布尔值和 None 做转换
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.lower() == "none":
        value = None
    config[key] = value
    save_config(config)
