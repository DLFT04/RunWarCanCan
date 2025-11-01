## 只是一个网络信息查询工具

###### RunWarCanCan v0.1.0

一个多功能 Python 工具，用于快速查询 IP 信息、ICP 备案、CDN 状态以及域名 Whois 信息。

#### 实现了以下功能

- CDN 检测：通过域名进行多地节点并发检测，判断是否存在 CDN
- IP 查询：根据 IP 或域名获取地址归属地及绑定网站信息
- ICP 查询：自动获取 ICP 备案号、主办单位与备案时间
- Whois 查询：解析域名注册人、注册时间、DNS 等详细信息
- 代理支持：可选网络代理参数，适配受限网络环境
- 日志输出：模块独立日志与彩色终端输出，便于排查与记录

#### 环境配置

开发环境：Python 3.13.1
推荐使用 Python 3.13+。建议使用虚拟环境隔离依赖

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### 使用示例

获取帮助

```bash
python main.py --help
```

获取配置帮助

```bash
python main.py config --help
```

查询 IP

```bash
python main.py ip 114.114.114.114
```

查询 ICP 备案信息

```bash
python main.py icp baidu.com
```

查询 whois 信息

```bash
python main.py whois baidu.com
```

查询 CDN 是否存在

```bash
python main.py cdn baidu.com
```

#### 目录结构(有点烂但后续会修改)

```
RunWarCanCan/
├── documents/ # 文档目录
├── services/ # 各查询模块
│ ├── cdn.py
│ ├── icp.py
│ ├── ip.py
│ ├── logger.py
│ └── whois.py
├── log/ # 日志输出目录
│ ├── cdn/
│ ├── icp/
│ ├── ip/
│ ├── whois/
│ ├── config.log
│ ├── err.log
│ └── main.log
├── config_manager.py # 配置管理模块
├── config.json # 默认配置文件
├── main.py # 程序主入口
├── README.md
└── requirements.txt
```

#### 致谢

- 某 wx 群的大佬提供的 go 安全工具开发教程，这让我知道了要实现什么东西
- [部分 ICP 查询逻辑参考自[xiiiii1/icpapi](https://github.com/xiiiii1/icpapi/tree/main), 在此基础上进行了重构与扩展(确信)
- 不可避免使用的一系列 AI 工具
- AND YOU
