from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from .logger import get_logger
from typing import Optional

def query_icp(keyword: str, log_path: Optional[str] = None, proxy: Optional[str] = None):
    """
    完成从域名到 ICP 信息的完整查询流程：
        1. 获取初始 acw_tc cookie 并生成请求 headers
        2. 获取 ASP cookies 并组合到 headers
        3. 刷新缓存以获取最新 ICP 数据
        4. 请求 ICP 页面并解析 HTML 表格
        5. 将每条记录打印并通过 logger 输出

    Args:
        keyword (str): 查询域名或关键词
        log_path (Optional[str]): 日志存储路径
        proxy (Optional[str]): HTTP/HTTPS 代理地址，例如 'http://127.0.0.1:7890'

    """
    logger = get_logger(name="icp", log_path=log_path if log_path is not None else None)
    logger.info(f"开始查询 ICP: {keyword}")

    search_url = f"https://www.beianx.cn/search/{keyword}"
    cache_url = f"https://www.beianx.cn/up_cache_2025/ajax_get2?type=&keyword={keyword}"
    proxies = {"http": proxy, "https": proxy} if proxy else None

    # 1. 获取 acw_tc cookie
    resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies)
    cookie_str = resp.headers.get("Set-Cookie", "")
    logger.debug(f"初始响应Cookie: {cookie_str}")

    acw_tc = ""
    if "acw_tc=" in cookie_str:
        acw_tc_value = cookie_str.split(";")[0]
        acw_tc = f"{acw_tc_value}; mac_string=13d71b22a4-569a-4b7e-a6f6-6f2de6140a83"
        logger.debug(f"生成 acw_tc cookie: {acw_tc}")

    # 2. 获取 ASP Cookie
    headers = {"User-Agent": "Mozilla/5.0"}
    if acw_tc:
        resp2 = requests.get(search_url, headers={"Cookie": acw_tc, "User-Agent": "Mozilla/5.0"}, proxies=proxies)
        set_cookie = resp2.headers.get("Set-Cookie", "")
        asp_cookies = {m.group(1).strip(): m.group(2).strip()
                       for item in set_cookie.split(', ') if ".AspNet" in item
                       for m in [re.match(r"([^=]+)=([^;]*);?", item)] if m}
        combined_cookie = acw_tc + ";" + ";".join(f"{k}={v}" for k, v in asp_cookies.items())
        headers["Cookie"] = combined_cookie

    # 3. 刷新缓存
    try:
        resp_cache = requests.get(cache_url, headers=headers, proxies=proxies, timeout=20)
        if '"msg":"更新成功"' in resp_cache.text:
            logger.info("刷新缓存成功")
        else:
            logger.warning(f"刷新缓存失败: {resp_cache.status_code}")
    except Exception as e:
        logger.error(f"刷新缓存异常: {e}")

    # 4. 请求 ICP 页面
    try:
        resp_final = requests.get(search_url, headers=headers, proxies=proxies, timeout=15)
        resp_final.raise_for_status()
    except Exception as e:
        logger.error(f"ICP 页面请求失败: {e}")
        return []

    # 5. 解析数据
    results = []
    try:
        soup = BeautifulSoup(resp_final.text, 'html.parser')
        rows = soup.find('table', class_='table').find_all('tr')[1:]
        logger.info(f"找到 {len(rows)} 行数据")
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 7:
                item = {
                    "company": cells[1].get_text(strip=True),
                    "domain": cells[5].get_text(strip=True),
                    "icp_number": cells[3].get_text(strip=True),
                    "audit_date": cells[6].get_text(strip=True)
                }
                results.append(item)
                logger.info(
                    f"域名 {keyword} 查询结果:\n"
                    "+------------------+------------------------\n"
                    f"| 主办单位名称     | {item['company']:<24}\n"
                    f"| ICP备案号        | {item['icp_number']:<24}\n"
                    f"| 网站首页地址     | {item['domain']:<24}\n"
                    f"| 审核通过日期     | {item['audit_date']:<24}\n"
                    "+------------------+------------------------"
                )

    # 差错处理
    except Exception as e:
        logger.error(f"解析 ICP 数据失败: {e}")

    # 打印查询信息
    logger.info(f"查询完成，共 {len(results)} 条记录")


if __name__ == "__main__":
    test_domains = ["qq.com", "baidu.com"]
    for domain in test_domains:
        query_icp(domain, log_path=f"./logs/icp/{domain}.icp.log")
