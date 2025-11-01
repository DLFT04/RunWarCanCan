## ip.py - IP 信息查询工具

基于 ip138 网站，实现对指定 IP 的信息查询，包括：

1. **IP 地址归属地解析**
2. **绑定域名及绑定时间查询**
3. **格式化输出查询结果**
4. **日志管理统一通过 logger 模块**

---

#### 数据结构说明：

IPRes 用于存储单个 IP 查询结果

```
@dataclass(class IpRes):
    address: str = "" # IP 归属地
    bind_times: List[str] = field(default_factory=list) # IP 被绑定的时间列表
    bind_sites: List[str] = field(default_factory=list) # IP 被绑定的网站列表
```

---

#### 函数说明：

### def format_ipres:

格式化单个 IP 查询结果为表格字符串，供日志或终端输出使用。

    Args:
        ip (str): 查询的 IP 地址
        res (IpRes): IP 查询结果对象

    Returns:
        str: 格式化后的 IP 信息表格

### def query_ip:

IP 查询主接口，通过请求 ip138 网站收集 IP 归属地及绑定信息，并将结果打印并通过日志系统保存。

    Args:
        ip (str): 目标 IP 地址
        log_path (Optional[str]): 日志存储路径
        proxy (Optional[str]): HTTP/HTTPS 代理

    Returns:
        IpRes: 单 IP 查询结果对象
