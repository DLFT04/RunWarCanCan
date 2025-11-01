### 关于 config 的配置说明

通过以下命令进行配置，或直接修改 config.json

```bash
python main.py config --set-key [key] --set-value [value]
```

---

当前支持以下配置：

```python
DEFAULT_CONFIG = {
    "level": "DEBUG",       # 日志级别
    "use_color": True,      # 是否彩色输出日志
    "output_json": False,   # 是否输出 JSON 格式
    "name": None,           # 可选日志名
    "log":True,             # 是否启用日志输出
    "log_path": "./log",    # 日志输出路径, 此为根路劲
    "proxy": None,          # 代理设置, 如http://127.0.0.1:7890
    "show_logo": True       # 展示工具logo
}
```
