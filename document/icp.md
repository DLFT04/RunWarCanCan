## ~~ICP 查询模块~~[^awful]

该模块用于通过 beianx.cn 网站查询指定域名的 ICP 备案信息，包括：

1.  **获取必要的 cookies（acw_tc 与 ASP cookies）**
2.  **刷新缓存以确保数据最新**
3.  **请求 ICP 查询页面**
4.  **解析页面表格，打印并记录查询结果**

---

### ICP 查询函数 def query_icp

    该函数完成从域名到 ICP 信息的完整查询流程：
        1. 获取初始 acw_tc cookie 并生成请求 headers
        2. 获取 ASP cookies 并组合到 headers
        3. 刷新缓存以获取最新 ICP 数据
        4. 请求 ICP 页面并解析 HTML 表格
        5. 将每条记录打印并通过 logger 输出

    Args:
        keyword (str): 查询域名或关键词
        log_path (Optional[str]): 日志存储路径
        proxy (Optional[str]): HTTP/HTTPS 代理地址，例如 'http://127.0.0.1:7890'

[^awful]: 这一脚本实现思路主要[来源于此](https://github.com/xiiiii1/icpapi)但是给我实现成了一坨，下版本就重构。
