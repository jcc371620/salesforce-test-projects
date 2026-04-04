# salsforce-test-projects
- Prompt Engineer: 从零搭建一个简单项目，要求结合salesforce+Python + Pytest + Request + SQL + Playwright + pytest-bdd。一步一步教我，最简单的case。我用的trailhead playground

搭建一个结合 Salesforce API 与 UI 自动化 的端到端（E2E）测试框架是一个非常实用的练习。我们将使用 Playwright 处理 UI，Requests 处理 API，并用 pytest-bdd 编写业务逻辑。

项目核心思路
API 部分：通过 Python 的 requests 调用 Salesforce REST API 快速创建测试数据。
UI 部分：使用 Playwright 登录 Trailhead Playground 验证数据是否在页面显示。
BDD 部分：使用自然语言描述测试步骤。

# 项目架构

## 连接Salesforce步骤
1. Create Playground: Trailhead -> Hands-On Orgs -> Create Playground
2. Launch Playground
3. Reset Password: Setup -> Quick Find -> Users -> Select User -> Reset Password
4. Get Security Token: Photo -> Setting -> Reset My Security Token
5. Get API Version: Setup -> Apex Classes -> New -> Version Settings -> Salesforce.com API
6. Get Current My Domain URL: Setup -> Company Settings -> My Domain
- Salesforce 官方 API 文档页面: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_versions.htm
- UI 界面地址： https://xxxx-dev-ed.lightning.force.com/ （这是给人类看的）
- 修改为API 基础地址： https://xxxx-dev-ed.my.salesforce.com/ （这是给代码跑自动化和发请求看的）
- Username: 
- Security token (case-sensitive): 
- password:

## 创建虚拟环境
1. 创建虚拟环境 (在你的项目根目录)
- python3 -m venv venv

2. 激活虚拟环境
- source venv/bin/activate # Mac/Linux

3. 此时你的开头会多一个 (venv) 标志，直接用 pip 即可
- pip install python-dotenv simple-salesforce pytest

## 安装依赖
- pip install pytest pytest-bdd playwright requests python-dotenv simple-salesforce
- playwright install chromium