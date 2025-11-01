import typer
import logging
from services import *
from config_manager import load_config, update_config
from pathlib import Path

app = typer.Typer(help="""
    多功能网络信息查询工具(支持IP/ICP/WHOIS/CDN查询) v0.1.0              
    """)
CONFIG_DESC = {
    "level": "日志等级: DEBUG / INFO / WARNING / ERROR / CRITICAL",
    "use_color": "是否使用彩色输出",
    "output_json": "是否输出 JSON 格式日志",
    "name": "Logger 名称",
    "log": "是否启用日志记录",
    "log_path": "日志根目录",
    "proxy": "默认代理地址 (可选)",
    "show_logo": "是否在 CLI 启动时显示 Logo",
}

@app.command()
def ip(domain: str):
    """根据 IP   查询 IP 地址信息   试试 python main.py ip 114.114.114.114"""
    logger.info(f"开始 IP 查询: {domain}")
    ip_log_path = log_root / "ip" /f"{domain}.ip.log"
    query_ip(domain, str(ip_log_path), proxy)


@app.command()
def icp(domain: str):
    """根据 域名 查询 ICP 备案信息  试试 python main.py icp baidu.com"""
    logger.info(f"开始 ICP 查询: {domain}")
    icp_log_path = log_root / "icp" / f"{domain}.icp.log"
    query_icp(domain, str(icp_log_path), proxy)


@app.command()
def whois(domain: str):
    """根据 域名 查询 WHOIS 信息    试试 python main.py whois qq.com"""
    logger.info(f"开始 WHOIS 查询: {domain}")
    whois_log_path = log_root / "whois" / f"{domain}.whois.log"
    query_whois(domain, str(whois_log_path))


@app.command()
def cdn(domain: str):
    """根据 域名 查询 CDN 节点      试试 python main.py cdn baidu.com"""
    logger.info(f"开始 CDN 查询: {domain}")
    cdn_log_path = log_root / "cdn" / f"{domain}.cdn.log"
    uutool(domain, str(cdn_log_path), proxy)


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="显示当前配置"),
    set_key: str = typer.Option(None, "--set-key", help="要修改的配置项, 和 --set-value 配套使用"),
    set_value: str = typer.Option(None, "--set-value", help="配置项的新值, 和 --set-key 配套使用")
):
    """查看或修改配置文件           试试 python main.py config --help"""
    config = load_config()
    if show:
        typer.echo("当前配置内容:")
        for k, v in config.items():
            desc = CONFIG_DESC.get(k, "")
            typer.echo(f"{k}: {v}  # {desc}")
        return

    if set_key and set_value is not None:
        if set_key not in config:
            typer.echo(f"配置项 {set_key} 不存在，请使用已有配置项: {list(config.keys())}")
            raise typer.Exit()
        update_config(set_key, set_value)
        typer.echo(f"配置已更新: {set_key} = {set_value}")
        config_logger.info(f"修改配置: {set_key} = {set_value}")
    else:
        typer.echo("请使用 --set-key 和 --set-value 来修改配置，或使用 --show 查看配置")

def get_path_log(log_root: Path, config: dict):
    # 日志文件
    main_log_path = log_root / "main.log"
    config_log_path = log_root / "config.log"
    err_log_path = log_root / "err.log"

    # 确保目录存在
    log_root.mkdir(parents=True, exist_ok=True)

    # 各模块日志目录
    module_dirs = ["ip", "icp", "whois", "cdn"]

    for d in module_dirs:
        (log_root / d).mkdir(exist_ok=True)
    logger = init_logger(
        level=getattr(logging, config.get("level", "DEBUG")),  # "DEBUG" -> logging.DEBUG
        use_color=config.get("use_color", True),
        output_json=config.get("output_json", False),
        log_path=str(main_log_path),
        name=config.get("name", None)
    )
    config_logger = get_logger("config", config_log_path)
    init_err_path(err_log_path=err_log_path)
    return logger, config_logger

if __name__ == "__main__":
    config = load_config()
    if config.get("show_logo"):
        print(r'''
    _____   
    |  __ \   
    | |__) |   _ _ __   __      ____ _ _ __ 
    |  _  / | | | '_ \  \ \ /\ / / _` | '__|
    | | \ \ |_| | | | |  \ V  V / (_| | |   
    |_|  \_\__,_|_| |_|   \_/\_/ \__,_|_|   
    ___ __ _ _ __     ___ __ _ _ __       
    / __/ _` | '_ \   / __/ _` | '_ \      
    | (_| (_| | | | | | (_| (_| | | | |     
    \___\__,_|_| |_|  \___\__,_|_| |_|
    ''')
    proxy = config.get("proxy")

     # 根日志目录
    log_root = config.get("log_path", "./logs")  # 默认值
    log_root = Path(log_root)  # 转成 Path 对象，后续可直接拼接

    logger, config_logger = get_path_log(log_root, config)
    import sys
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    app()
