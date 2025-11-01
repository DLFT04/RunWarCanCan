"""
cdn.py - 多节点 CDN 检测工具

提供对指定 IP/域名的 CDN 状态检测，包括：
1. 多地节点并发请求
2. 收集 IP 列表及数量
3. 格式化日志输出检测表格
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Optional
from .logger import get_logger
import requests

@dataclass
class CDNResult:
    '''单个 CDN 节点的检测结果'''
    region: str
    status: str = ""
    ip_count: int = 0
    ip_list: List[str] = field(default_factory=list)

# 多地 ping 节点表格
CDN_NODES = {
    "https://ips-app-nnrrjaztiz.cn-qingdao.fcapp.run":      "中国-青岛",
    "https://ips-app-vrdhcyxprn.ap-southeast-5.fcapp.run": "新加坡",
    "https://ips-app-vrdhcyxprn.eu-west-1.fcapp.run":      "欧洲-伦敦",
    "https://ips-app-vrdhcyxprn.eu-central-1.fcapp.run":   "欧洲-法兰克福",
    "https://ips-app-vrdhcyxprn.ap-southeast-7.fcapp.run": "印度尼西亚-雅加达",
    "https://ips-app-vrdhcyxprn.ap-southeast-1.fcapp.run": "印度尼西亚-雅加达",
    "https://ips-app-vrdhcyxprn.ap-southeast-3.fcapp.run": "印度尼西亚-雅加达",
    "https://ips-app-nnrrqmtriz.cn-shenzhen.fcapp.run":    "中国-深圳",
    "https://ips-app-vrdhcyxprn.cn-chengdu.fcapp.run":     "中国-成都",
    "https://ips-app-nnrrjaztiz.cn-hangzhou.fcapp.run":    "中国-杭州",
    "https://ips-app-vrdhcyxprn.cn-zhangjiakou.fcapp.run": "中国-张家口",
    "https://ips-app-vrdhcyxprn.ap-northeast-2.fcapp.run": "韩国-首尔",
    "https://ips-app-nnrrjaztiz.cn-beijing.fcapp.run":     "中国-北京",
    "https://ips-app-vrdhcyxprn.cn-huhehaote.fcapp.run":   "中国-呼和浩特",
    "https://ips-app-nnrrjaztiz.cn-hongkong.fcapp.run":    "中国-香港",
    "https://ips-app-nnrrjaztiz.cn-qingdao.fcapp.run":     "中国-青岛",
}

def fetch_cdn_node(logger, ip: str, url: str, region: str, proxy: Optional[str] = None, timeout: int = 10) -> CDNResult:
    '''请求单个节点，返回 IP 信息'''
    result = CDNResult(region=region)
    proxies = {"http": proxy, "https": proxy} if proxy else None
    proxy_info = "无代理" if proxies is None else f"代理: {list(proxies.values())[0]}"
    logger.info(f"正在请求: {url:<52} | 目标: {ip} | {proxy_info}")

    # 请求节点并处理返回信息
    try:
        # 发送请求并接收原始响应数据
        resp = requests.get(url, params={"domain": ip}, timeout=timeout, proxies=proxies)
        resp.encoding = 'UTF-8'
        resp.raise_for_status()

        # 处理接收的数据
        if resp.text:
            ip_list = [ip.strip() for ip in resp.text.split(",") if ip.strip()]
            result.ip_list = ip_list
            result.ip_count = len(ip_list)
            result.status = "检测成功"
        else:
            result.status = "无响应"

    # 差错处理
    except requests.Timeout:
        result.status = "超时" 
    except requests.RequestException as e:
        logger.error(f"请求失败: {url}, {e}")
        result.status = "检测失败"

    # 返回 ping 结果
    return result

def log_results_table(results: List[CDNResult], ip: str, logger) -> None:
    '''格式化输出多节点检测结果表格'''
    logger.info(f"目标 {ip} 检测结果如下:")

    # 加载表格头部
    header = "+------------------+----------+---------------------------------------+------------+"
    lines = [header,
             "| 检测节点         | IP数量   | IP列表                                | 检测状态   |",
             header]

    # 通过循环加载表格主体
    failed_count = 0
    for res in results:
        ip_list_str = ", ".join(res.ip_list) if res.ip_list else "-"
        if len(ip_list_str) > 37:
            ip_list_str = ip_list_str[:34] + "..."
        ip_count = str(res.ip_count) if res.status == "检测成功" else "-"
        if res.status != "检测成功":
            failed_count += 1
        lines.append(f"| {res.region:<10} | {ip_count:^8} | {ip_list_str:<37} | {res.status:<10} |")

    # 表格封尾
    lines.append(header)

    # 打印多地 ping 结果表格
    for line in lines:
        logger.info(line)

    # 检测失败时打印失败结果
    if failed_count == len(results):
        logger.warning(f"所有节点检测均失败，目标 {ip} 可能没有使用CDN")

def uutool(ip: str, log_path: Optional[str] = None, proxy: Optional[str] = None, max_workers: int = 5):
    '''多节点 CDN 检测主接口'''
    # 获取 logger 对象
    logger = get_logger("cdn_query", log_path=log_path)

    # 多线程进行 ping 请求并收集 ping 结果
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_cdn_node, logger, ip, url, region, proxy)
                   for url, region in CDN_NODES.items()]
        results = [f.result() for f in as_completed(futures)]

    # 打印结果
    log_results_table(results, ip, logger)

if __name__ == "__main__":
    test_ips = ["google.com"]
    proxy = 'http://127.0.0.1:7890'
    for ip in test_ips:
        print(f"\n========================= 查询 IP: {ip} =========================")
        uutool(ip, proxy)
