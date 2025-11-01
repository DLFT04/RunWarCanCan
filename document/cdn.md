## cdn.py - 多节点 CDN 检测工具

基于 UUtool 的 CDN 检测功能网页实现对指定域名的 CDN 状态检测，包括：

1. **多地节点并发请求**
2. **收集 IP 列表及数量**
3. **格式化日志输出检测表格**

---

#### 数据结构说明：

CDNResult 用于存储单个 CDN 节点的检测结果

```
@dataclass(class CDNResult):
    region: str # 节点所属地区
    status: str = "" # 检测状态，如 "检测成功"、"无响应"、"超时"
    ip_count: int = 0 # 返回 IP 数量
    ip_list: List[str] = field(default_factory=list) # 返回的 IP 列表
```

CDN 检测节点表格[^point_1]

```
CDN_NODES = {
    "https://ips-app-nnrrjaztiz.cn-qingdao.fcapp.run":      "中国-青岛",
    "https://ips-app-vrdhcyxprn.ap-southeast-5.fcapp.run": "新加坡",
    "https://ips-app-vrdhcyxprn.eu-west-1.fcapp.run":      "欧洲-伦敦",
    ...
}
```

---

#### 函数和类说明:

### def fetch_cdn_node

请求单个 CDN 节点，接收并处理返回的 IP 信息

    Args:
        logger: logging.Logger 对象
        ip (str): 目标域名或 IP
        url (str): 节点请求 URL
        region (str): 节点地区
        proxy (Optional[str]): HTTP/HTTPS 代理
        timeout (int): 请求超时时间（秒）

    Returns:
        CDNResult: 单节点检测结果

### def log_results_table

格式化输出多地 ping 检测结果表格[^awful_1]。

    Args:
        results (List[CDNResult]): 多节点检测结果列表
        ip (str): 查询目标
        logger: logging.Logger 对象

### def uutool

CDN 检测主接口，通过多线程调用 fetch_cdn_node()进行多地 ping 检测[^awful_2]并最后通过 log_results_table 输出结果[^awful_3]。

    Args:
        ip (str): 目标域名
        log_path (Optional[str]): 日志存储路径
        proxy (Optional[str]): 代理
        max_workers (int): 并发线程数

[^point_1]: CDN 节点检测表基于 UUtool 多地 ping 节点实现，以后万一不能用了可能需要大佬们自便，或者我发现了会尝试更新。
[^awful_1]: 这里没用处理表格的库所以打印出来的结果有些不好看，以后有时间会优化的。
[^awful_2]: 这里是用多线程 + requests 实现的，用 aiohttp 或许会更好，以后有时间会优化的。
[^awful_3]: 现版本最大线程数 max_workers 定死了是 5，以后有时间会优化的。
