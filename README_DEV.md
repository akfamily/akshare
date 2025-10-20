# 本地开发环境与测试指南（基于 AKShare）

目标：每天更新中国 A 股（股票与 ETF）日线数据，存入本地数据库，并用这些数据进行历史回测或模拟实盘测试。

主要文件：
- requirements-dev.txt            # 开发与运行所需 pip 包
- fetch_daily.py                 # 抓取并写入 SQLite 的脚本（主抓取脚本）
- db_utils.py                    # 数据库存取与表结构工具
- backtest_sma.py                # 简单 SMA 策略回测脚本
- codes.csv                      # （示例）需要抓取的股票/ETF 列表（你可以自定义）
- akshare-fetch.service          # systemd 单元示例（可选）
- start_fetch.sh                 # 简单 shell wrapper（可选）

一、准备与安装
1. 克隆你的仓库（如果尚未）：
   git clone https://github.com/jackerman8026/akshare.git
   cd akshare

2. 创建并激活虚拟环境（推荐）：
   python3 -m venv .venv
   source .venv/bin/activate

3. 安装依赖：
   pip install --upgrade pip
   pip install -r requirements-dev.txt

4. 安装本仓库（开发模式）：
   python -m pip install -e .

二、准备代码列表
- 编辑 `codes.csv`（或用 akshare 的接口自动拉取代码）。codes.csv 示例格式：每行一个代码，如：
  000001
  600519
  510300

三、初始化与第一次抓取（手动）
- 运行抓取脚本（示例：抓取最近 365 天）：
  mkdir -p data
  python fetch_daily.py --codes codes.csv --db data/akshare.db --start $(date -d '365 days ago' +%Y%m%d) --end $(date +%Y%m%d)

四、定时抓取（每日更新）
选项 A：用 systemd timer（推荐生产）
- 把 akshare-fetch.service 放到 /etc/systemd/system/ 并启用（见示例）

选项 B：crontab
- crontab -e
  添加行（每天 16:30 运行）：
  30 16 * * * /home/jackerman8026/akshare/.venv/bin/python /home/jackerman8026/akshare/fetch_daily.py --codes /home/jackerman8026/akshare/codes.csv --db /home/jackerman8026/akshare/data/akshare.db --start 20200101 --end $(date +\%Y\%m\%d) >> /home/jackerman8026/akshare/logs/fetch.log 2>&1

五、回测（示例策略）
- 运行：
  python backtest_sma.py --code 000001 --db data/akshare.db --start 20180101 --end 20241001 --short 10 --long 50

六、常见问题与调优
- 如果 ak.stock_zh_a_hist 返回中文列名，脚本会自动映射到英文列名。若 akshare API 名称在你的版本中不同，请告知我，我可以调整映射。
- 建议把数据库文件放在带持久化的路径（非 /tmp）。
- 若需要并行抓取（大量代码），可以改造 fetch_daily.py 使用 concurrent.futures.ThreadPoolExecutor，但注意频率限制与目标网站封 IP 的风险，生产请使用代理或限速与重试策略.