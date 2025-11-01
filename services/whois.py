import whois
from .logger import get_logger
from typing import Optional

def query_whois(domain: str, log_path: Optional[str] = None) -> None:
    """查询域名Whois信息并通过日志输出"""

    # 初始化Whois模块专属日志器
    logger = get_logger("whois_query", log_path=log_path)

    try:
        # 调用whois库查询并格式化结果
        result = whois.whois(domain)

        result_str = "\n".join([f"{k}: {v}" for k, v in result.items() if v is not None])
        logger.info(f"Whois查询结果:\n{result_str}")

    # 差错处理
    except Exception as e:
        logger.error(f"Whois查询错误: {str(e)}")


# 测试用例
if __name__ == "__main__":
    test_domains = ["google.com", "baidu.com"]
    
    for domain in test_domains:
        print(f"\n===== 查询域名: {domain} =====")
        query_whois(domain)
        