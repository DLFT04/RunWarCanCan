from .logger import get_logger
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class IpRes:
    # 存储单个 IP 查询结果
    address: str = ""
    bind_times: List[str] = field(default_factory=list)
    bind_sites: List[str] = field(default_factory=list)

def format_ipres(ip: str, res: IpRes) -> str:
    """
    格式化单个 IP 查询结果为表格字符串，供日志或终端输出使用。

    Args:
        ip (str): 查询的 IP 地址
        res (IpRes): IP 查询结果对象

    Returns:
        str: 格式化后的 IP 信息表格
    """

    # 加载 IP 归属地信息
    lines = []
    lines.append(f"\n+-----------------+------------------------")
    lines.append(f"| IP地址          | {ip:<24}")
    lines.append(f"| 归属地          | {res.address:<24}")
    lines.append(f"+-----------------+------------------------")

    # 加载 IP 绑定信息
    if res.bind_sites:
        lines.append("绑定信息:")
        lines.append("+--------------------------------+--------------------------------+")
        for site, time in zip(res.bind_sites, res.bind_times):
            lines.append(f"| {site:<30} | {time:<30} |")
        lines.append("+--------------------------------+--------------------------------+")
    else:
        lines.append("未查到相关绑定信息！")

    # 将表格返回
    return "\n".join(lines)

def query_ip(ip: str, log_path: Optional[str] = None, proxy: Optional[str] = None):
    '''
    IP 查询主接口，通过请求 ip138 网站收集 IP 归属地及绑定信息，并将结果通过日志打印。

    Args:
        ip (str): 目标 IP 地址
        log_path (Optional[str]): 日志存储路径
        proxy (Optional[str]): HTTP/HTTPS 代理

    Returns:
        IpRes: 单 IP 查询结果对象

    '''

    # 加载 logger 对象用于管理日志
    logger = get_logger("ip_query", log_path=log_path)

    # 配置响应头，ip138网站请求需要一个正常的 User-Agent头
    res = IpRes()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}

    try:
        # 如果有代理需求，配置代理
        proxies = {"http": proxy, "https": proxy} if proxy else None

        # 收发请求
        r = requests.get(f"https://site.ip138.com/{ip}/", proxies=proxies, headers=headers)
        r.raise_for_status()

        # 对响应报文信息进行处理，精确找到数据位置
        soup = BeautifulSoup(r.text, "lxml")
        res.address = soup.find("h3").text.strip()
        items = soup.select("#list li")[2:]
        for item in items:
            date = item.select_one(".date").text.strip() if item.select_one(".date") else ""
            site = item.select_one("a").text.strip() if item.select_one("a") else ""
            if date and site:
                res.bind_times.append(date)
                res.bind_sites.append(site)

        # 将结果打印并保存
        logger.info(format_ipres(ip, res))

    # 差错处理
    except Exception as e:
        logger.error(f"IP查询错误: {e}", exc_info=True)

    return res

if __name__ == "__main__":
    # 测试 IP 列表
    test_ips = ["8.8.8.8", "114.114.114.114"]
    
    for ip in test_ips:
        print(f"\n===== 查询 IP: {ip} =====")
        res = query_ip(ip)
