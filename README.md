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
7. OAuth: setup -> OAuth and OpenID Connect Settings -> Allow
8. Setup-> App Manager -> New External Client App -> Consumer Key and Secret
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
- pip install pytest-playwright
- playwright install chromium

## 安装插件
- Cucumber (Gherkin) Full Support

## 运行方法
- 使用 pytest 运行，-s 参数是为了看到 print 打印出来的“成功”信息
- pytest -s test_connection.py

## 逻辑解析
1. API 阶段 (无感秒杀)：
Python 会通过 simple-salesforce 静默连接到你的 Playground。
它会先执行一个 SOQL (SQL) 查询：SELECT Id FROM Contact WHERE LastName = 'Gemini_Test_User'。
如果找到了旧数据，它会直接调用 REST API 的 DELETE 方法删掉。
然后调用 POST 方法创建一个崭新的联系人。
终端会打印：API 创建成功, ID: 003xxxxxx。

2. UI 阶段 (Playwright 接管)：
浏览器窗口自动弹出，自动输入你在 .env 里的用户名和密码。
登录成功后，它会直接跳转到 Contact 列表页。
验证：Playwright 会在页面 DOM 树中寻找刚才 API 创建的那个名字。

3. BDD 报告：
如果一切顺利，你会看到绿色的 3 passed

## Problems
1. vpn问题/网络/SSL 握手拦截 问题。这个 SSL_ERROR_SYSCALL 通常是因为你的本地 Git 客户端在通过 HTTPS 协议连接 GitHub 时，被系统代理、防火墙或不稳定的 VPN 节点强行中断了连接。
- git config --global --unset http.proxy
- git config --global --unset https.proxy