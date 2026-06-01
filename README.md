# Vibe-coding-

这是一个面向金融AI产品方向的 Vibe Coding 作品集，包含 4 个完整可运行项目，覆盖数据可视化、大模型应用、自动化工具与效果评测等方向，展示了从业务需求到技术落地的完整开发能力。

---

## 项目列表

### index.html
主作品集页面，用于简历投递展示。
- 整合 4 个项目的介绍、技术栈和在线演示链接
- 统一的风格设计，适配求职场景
- 响应式布局，支持多端访问

---

### project1-dashboard.html  
金融市场情绪仪表盘
- 核心功能：实时展示大盘走势、行业涨跌热力图、北向资金流向与市场情绪指数，支持多图表联动
- 技术栈：HTML、TailwindCSS、JavaScript、ECharts
- 亮点：将投研人员每日市场跟踪时间从 30 分钟缩短至 5 分钟，数据可视化直观易懂
- 使用方式：直接打开 HTML 文件即可查看完整演示

---

### project2-report-agent.html
AI财报智能分析Agent
- 核心功能：支持 PDF 财报上传、解析与关键财务指标提取，内置 3 个行业头部公司示例，可通过自然语言提问获取结构化分析结果
- 技术栈：Python、Streamlit、DeepSeek API、PyPDF2、HTML、JavaScript
- 亮点：10 分钟即可完成分析师一天的财报分析工作，降低专业门槛
- 使用方式：
  1. 前端演示：直接打开 HTML 文件
  2. 后端运行：
     ```bash
     pip install streamlit PyPDF2 openai
     streamlit run app.py

---

### project3-toolkit.html
投研工作流自动化工具箱
- 核心功能：包含财报批量下载、Excel 格式统一、财务指标计算、行业对比分析等多个投研高频自动化工具
- 技术栈：Python、Pandas、Requests、OpenPyXL
- 亮点：将重复工作效率提升 80% 以上，支持单文件脚本直接运行
- 使用方式：运行对应 Python 脚本即可使用工具功能

---

### project4-eval-platform.html
Agent 效果评测平台
- 核心功能：金融场景 AI 应用评测工具，支持多模型、多 Prompt 批量对比测试，自动生成可视化评测报告
- 技术栈：Python、Streamlit、Pandas、Matplotlib
- 亮点：建立了完整的 Agent 与模型评测体系，用数据驱动产品优化
- 使用方式：运行对应脚本即可使用评测功能

---

## 技术栈总览
- 前端：HTML、TailwindCSS、JavaScript
- 后端：Python、Streamlit
- 数据可视化：ECharts、Matplotlib
- 大模型：DeepSeek API
- 数据处理：Pandas、PyPDF2、OpenPyXL
