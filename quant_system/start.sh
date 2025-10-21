#!/bin/bash
# A股量化系统 - 一键启动脚本（Mac/Linux）

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║          📊 A股量化分析系统 - 启动助手                   ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查Python
echo -e "${YELLOW}检查环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3未安装${NC}"
    echo "请先安装Python3: brew install python"
    exit 1
fi
echo -e "${GREEN}✓ Python3已安装: $(python3 --version)${NC}"

# 检查依赖
echo -e "${YELLOW}检查依赖包...${NC}"
python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}! 缺少依赖包，正在安装...${NC}"
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi
echo -e "${GREEN}✓ 依赖包已就绪${NC}"

echo ""
echo "请选择操作："
echo ""
echo "  ${BLUE}1${NC}) 🧪 运行测试"
echo "  ${BLUE}2${NC}) 📊 生成每日报告"
echo "  ${BLUE}3${NC}) 🌐 启动Web界面"
echo "  ${BLUE}4${NC}) 💾 下载历史数据"
echo "  ${BLUE}5${NC}) 📖 查看使用示例"
echo "  ${BLUE}6${NC}) 🔄 全部运行（测试+报告+Web）"
echo "  ${BLUE}0${NC}) 退出"
echo ""

read -p "请输入选项 [0-6]: " choice

case $choice in
    1)
        echo -e "${BLUE}运行测试...${NC}"
        python3 test_simple.py
        ;;
    2)
        echo -e "${BLUE}生成每日报告...${NC}"
        python3 main.py
        echo -e "${GREEN}报告已生成，保存在 reports/ 目录${NC}"
        read -p "是否查看报告？(y/n): " view
        if [ "$view" = "y" ]; then
            cat reports/daily_report_*.txt | tail -100
        fi
        ;;
    3)
        echo -e "${BLUE}启动Web界面...${NC}"
        echo ""
        echo -e "${GREEN}访问地址: http://localhost:8501${NC}"
        echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
        echo ""
        streamlit run web_app.py
        ;;
    4)
        echo -e "${BLUE}下载历史数据...${NC}"
        python3 scripts/download_data.py
        ;;
    5)
        echo -e "${BLUE}运行使用示例...${NC}"
        python3 examples/basic_usage.py
        ;;
    6)
        echo -e "${BLUE}全部运行...${NC}"

        echo ""
        echo -e "${YELLOW}[1/3] 运行测试...${NC}"
        python3 test_simple.py

        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${YELLOW}[2/3] 生成报告...${NC}"
            python3 main.py

            echo ""
            echo -e "${YELLOW}[3/3] 启动Web界面...${NC}"
            echo ""
            echo -e "${GREEN}访问地址: http://localhost:8501${NC}"
            echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
            echo ""
            streamlit run web_app.py
        else
            echo -e "${RED}测试失败，请检查环境${NC}"
        fi
        ;;
    0)
        echo -e "${GREEN}再见！${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}无效选项${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}完成！${NC}"
