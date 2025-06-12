# Knowledge Graph Generator

基于大语言模型LLM 的知识图谱生成工具，支持从文本中自动提取实体关系并可视化展示。
## demo
试用网址：https://knowledgegraph-app.streamlit.app/  
介绍文章：[使用大语言模型 + streamlit-agraph 生成和可视化知识图谱](https://mp.weixin.qq.com/s/HAIzAcODJZLL20eshMf3qQ)

## 项目介绍

本项目是一个基于大语言模型的知识图谱生成工具，可以自动从输入文本中提取实体和关系，并生成可视化的知识图谱。目前支持智谱 AI 和 Azure OpenAI 两种模型供应商。

### 主要特性

- 🤖 支持多个 LLM 供应商
  - Deepseek(新增)
  - 智谱 AI (GLM-4)
  - Azure OpenAI
- 📊 知识图谱可视化
  - 交互式图形界面
  - 节点和边的自定义样式
  - 支持图谱缩放和拖拽
- 🎯 简单易用的 Web 界面
  - Streamlit 构建的直观界面
  - 实时反馈和错误提示
  - 支持大段文本输入

## 安装说明

### 环境要求

- Python 3.8+
- pip
- langchain==0.3.25
- langchain-community==0.3.24
- langchain-core==0.3.64
- langchain-text-splitters==0.3.8
- langdetect==1.0.9
- streamlit==1.38.0
- streamlit-agraph==0.0.45
- zhipuai==2.1.5.20230904
- langchain_deepseek==0.1.3
### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/KnowledgeGraph-Streamlit.git
cd KnowledgeGraph-Streamlit
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run app.py
```

## 使用指南

### 配置 API
1. Deepseek
   - 访问 [Deepseek](https://api-docs.deepseek.com/zh-cn/)
   - 注册账号并创建应用
   - 获取 API 密钥
2. 智谱 AI
   - 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
   - 注册账号并创建应用
   - 获取 API 密钥

3. Azure OpenAI
   - 访问 [Azure Portal](https://portal.azure.com/)
   - 创建 Azure OpenAI 服务
   - 获取 API 密钥和配置信息

### 使用步骤

1. 启动应用后，在侧边栏：
   - 选择 LLM 供应商（默认为Deepseek）
   - 输入对应的 API 密钥

2. 在主界面：
   - 在文本框中输入待分析文本
   - 点击"生成知识图谱"按钮
   - 等待知识图谱生成
   - 查看可视化结果

### 示例输入

```text
人工智能是计算机科学的一个分支，它包含机器学习和深度学习两个重要领域。
机器学习使用统计方法来让计算机系统逐步改善性能，而深度学习则是基于神经网络的一种特殊机器学习方法。
```

## 项目结构

```
knowledge-graph-generator/
├── app.py              # 主应用程序
├── llm_utils.py        # LLM 调用工具
├── utils.py            # 通用工具函数
├── requirements.txt    # 项目依赖
└── README.md           # 项目文档
```

## 技术栈

- **前端框架**: Streamlit
- **图形可视化**: streamlit-agraph
- **LLM 接口**: 
  - langchain-community
  - Deepseek Azure OpenAI 
- **数据处理**: Python 标准库

## 注意事项

1. API 密钥安全
   - 不要在代码中硬编码 API 密钥
   - 建议使用环境变量管理密钥
   - 定期更换 API 密钥

2. 使用限制
   - 注意 API 调用频率限制
   - 单次文本长度限制
   - 知识图谱节点数量至少需要 3 个

3. 性能优化
   - 大文本建议分段处理
   - 适当调整模型参数
   - 缓存常用结果

## 常见问题

1. Q: 为什么图谱生成失败？
   A: 常见原因：
   - API 密钥无效或过期
   - 输入文本过短或实体关系不足
   - 网络连接问题

2. Q: 如何提高图谱质量？
   A: 建议：
   - 使用结构化的输入文本
   - 调整模型温度参数
   - 增加输入文本的实体密度

## 贡献指南
Tunnello 提供了主要的基础框架
getMoreAndMore(本人) 进行了一些优化，并新增了deepseek接口功能


## 致谢
感谢用户 Tunnello 开源的基础框架
感谢以下项目和工具：
- [Streamlit](https://streamlit.io/)
- [智谱 AI](https://open.bigmodel.cn/)
- [Azure OpenAI](https://azure.microsoft.com/products/cognitive-services/openai-service/)
```
