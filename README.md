# salsforce-test-projects
- Prompt Engineer: 从零搭建一个简单项目，要求结合salesforce+Python + Pytest + Request + SQL + Playwright + pytest-bdd。一步一步教我，最简单的case。我用的trailhead playground

搭建一个结合 Salesforce API 与 UI 自动化 的端到端（E2E）测试框架是一个非常实用的练习。我们将使用 Playwright 处理 UI，Requests 处理 API，并用 pytest-bdd 编写业务逻辑。

## 项目核心思路
- 第一步：连通salesforce -- Done
- 第二步：创建测试数据
- 第三步：尝试批量Query（select），主要用途是data validation
- 第四步：尝试批量edit/delete/update
- 第四步：搭建lwc组件
- 第五步：尝试playwright模拟真实用户操作ui页面
- API 部分：通过 Python 的 requests 调用 Salesforce REST API 快速创建测试数据。
- UI 部分：使用 Playwright 登录 Trailhead Playground 验证数据是否在页面显示。
- BDD 部分：使用自然语言描述测试步骤。

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
    - Python 会通过 simple-salesforce 静默连接到你的 Playground。
    它会先执行一个 SOQL (SQL) 查询：SELECT Id FROM Contact WHERE LastName = 'Gemini_Test_User'。
    如果找到了旧数据，它会直接调用 REST API 的 DELETE 方法删掉。
    然后调用 POST 方法创建一个崭新的联系人。
    终端会打印：API 创建成功, ID: 003xxxxxx。

2. UI 阶段 (Playwright 接管)：
    - 浏览器窗口自动弹出，自动输入你在 .env 里的用户名和密码。
    登录成功后，它会直接跳转到 Contact 列表页。
    验证：Playwright 会在页面 DOM 树中寻找刚才 API 创建的那个名字。

3. BDD 报告：
    - 如果一切顺利，你会看到绿色的 3 passed

## 疑问与拓展
1. 如何知道向哪个接口申请 Token？
- 这个地址（Endpoint）不是随机生成的，而是 Salesforce 官方定义的 OAuth 2.0 授权端点。
- 标准的通用地址：
    - 生产环境 / 开发者版 (Developer Edition)：https://login.salesforce.com/services/oauth2/token
    - 沙箱环境 (Sandbox)：https://test.salesforce.com/services/oauth2/token
- 地址的构成含义：
    - https://login.salesforce.com：这是域名，告诉请求发往哪个服务器群。
    - /services/oauth2/token：这是固定的路径。它告诉 Salesforce 系统：“我不是要登录网页，我是要调用 OAuth2 服务的 Token 生成功能”。
- 这个地址是怎么来的？
    - 它是根据 Salesforce 的 Web 预设规范 来的。当你创建一个 Connected App 时，Salesforce 就会激活这个接口来监听你的 client_id 和 client_secret。即便你使用了 My Domain（自定义域名，如 yourcompany.my.salesforce.com），上述通用地址依然有效，因为它们在后台是打通的。
---
2. 关于OAuth 2.0（Open Authorization）
- OAuth 2.0 是一个全球通用的行业标准协议。可以把它理解为互联网世界的“通用电子门禁标准”。无论是 Google、GitHub、微信、支付宝，还是你正在使用的 Salesforce，只要涉及“第三方应用获取数据”，几乎都在用这套协议。
- OAuth 2.0 的本质：授权（Authorization）
    - 它的核心作用是：在不泄露用户密码的前提下，授权第三方应用访问特定的资源。
    - 没有 OAuth 之前：如果你想让一个 Python 脚本读取你的 Salesforce 数据，你得把你的用户名和密码直接写在代码里。如果代码泄露了，你的整个账号就丢了。
    - 有了 OAuth 之后：Python 脚本通过一个“令牌（Token）”来访问。这个令牌是有时效的，而且只能干你允许它干的事（比如只能读数据，不能改密码）。
- 核心优势
    - 安全性：第三方应用永远拿不到你的真实密码。
    - 权限细分（Scopes）：你可以规定脚本只能看“联系人”，不能看“财务报表”。
    - 随时撤销：如果你觉得脚本有问题，可以直接在 Salesforce 后台停掉这个 Connected App，而不需要修改你的登录密码。
- Salesforce的使用
    - Connected App：这是 Salesforce 对 OAuth 协议的具体实现方式。你必须先在 Salesforce 里“注册”你的脚本，拿到 Consumer Key。
    - 安全防御：因为 Salesforce 承载的是企业的核心资产，所以它默认锁死了老旧的登录方式（如你遇到的 SOAP API 禁用），强制要求使用 OAuth 2.0 这种更安全的现代协议。
- 常见的 OAuth 2.0 例子
    - APP 扫码登录：当你在电脑上用“微信扫码登录”某个网站时，背后就是 OAuth 流程。
    - 第三方集成：比如在 Slack 里查看 Google Drive 的文件，或者用 GitHub 账号登录某个技术论坛。
- Authentication & Authorization
    - 认证 (Authentication) 是证明“你是谁”（输入账号密码），登录。
    - 授权 (Authorization) 是决定“你能干什么”（比如：允许这个 Python 脚本读取我的 Salesforce 客户名单）。比如给了一个Access Token，这个token只在特定时间内有效，也并非是账号密码，并且有权限范围/Scopes。
---
3. 关于consumer key和consumer secret
- 在 OAuth 2.0 的世界里，这两个东西合起来被称为 Client Credentials（客户端凭据）
- Consumer Key (客户标识符)
    - 角色：相当于 App 的用户名/ID（Public ID）。
    - 含义：它是一个公开的字符串，用来告诉 Salesforce：“嘿，我是那个叫 Python_Test_App 的程序，我来申请访问权限了。”
    - 安全性：虽然它不建议随处乱扔，但它本身并不是绝密信息。在 OAuth 流程中，它通常会出现在 URL 或请求体里。
- Consumer Secret (客户密钥)
    - 角色：相当于 App 的签名/密码（Private Key）。
    - 含义：它是用来证明“你真的是那个 App”的唯一凭证。
    - 安全性：绝对机密！ 只有你的 Python 脚本和 Salesforce 知道这个值。如果别人拿到了它，就可以伪装成你的 App 来窃取数据。这就是为什么我们要把它放进 .env 且不传到 GitHub 的原因。
- 它们是如何协同工作的？
    - （握手过程）当你运行 client.connect() 时，后台发生了以下对话：
    Python 脚本：“Salesforce，我是 ID 为 ABC...123 的 App（Consumer Key），这是我的防伪印章 XYZ...789（Consumer Secret）。现在有个用户（Username/Password）想授权我干活，请给个准话。”
    Salesforce：“收到。我查了一下，ABC...123 确实是我发出的 ID，印章 XYZ...789 也对得上。既然用户也给了密码，那这张**临时房卡（Access Token）**拿走吧。”
- 为什么不能只用用户名和密码？
    - 责任溯源：如果你的脚本写了个 Bug，疯狂删数据，Salesforce 可以根据 Consumer Key 直接停掉这个 App 的访问权，而不需要修改用户的登录密码（这样用户还能通过网页正常办公）。
    - 权限审计：管理员可以在后台看到：到底是“用户本人”在网页上操作，还是“Python 脚本”在后台操作。
    - 安全性隔离：即便你的脚本被黑了，泄露的也只是 App 的凭据，而不是用户的核心密码。
---
4. 关于SOAP API
- SOAP 全称是 Simple Object Access Protocol（简单对象访问协议）。
- 定义：
    - 它是一种基于 XML 的通信协议。你可以把它想象成一封“非常正式、格式死板的公文”。
- 特点：
    - 严格：必须遵循复杂的 XML 格式。
    - 笨重：哪怕只传输一个数字，也要套上好几层 XML 标签。
    - 强类型：对数据类型的定义非常死板，不容易出错但开发慢。
- Salesforce:
    - 并没有“彻底禁用” SOAP API，但在 2023 年至 2025 年间，Salesforce 在新出的环境（如你正在用的 Agentforce 或某些 Trial Org）中，默认关闭了 SOAP 登录权限。
    - 原因：SOAP 登录安全性较低（直接传账号密码），且不支持现代的多因素认证（MFA）。Salesforce 强制大家转向基于 REST 的 OAuth 2.0。
5. 关于REST API
- REST (Representational State Transfer) 是一种设计风格。如果把 SOAP 比作厚重的“纸质挂号信”，那么 REST 就是“发微信”。
- 特点：
    使用 HTTP 动词：它直接利用浏览器最常用的动作：GET（查）、POST（增）、PUT（改）、DELETE（删）。
    数据格式轻量：通常使用 JSON（像 Python 字典一样），而不是笨重的 XML。
    无状态：服务器不记你的“登录状态”，每次请求都必须带上你的“通行证”。

## Problems
1. vpn问题/网络/SSL 握手拦截 问题。这个 SSL_ERROR_SYSCALL 通常是因为你的本地 Git 客户端在通过 HTTPS 协议连接 GitHub 时，被系统代理、防火墙或不稳定的 VPN 节点强行中断了连接。
- 解决方案 1：
    1. 查看当前代理：在终端中运行以下命令，检查是否设置了代理：
    git config --global --get http.proxy
    git config --global --get https.proxy
    2. 取消代理：如果上述命令有输出，则运行以下命令清除代理设置：
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    3. 重试 Git 命令：取消后，再次执行 git clone 或 git pull，看问题是否解决。
- 解决方案 2:
    1. 如果你使用 HTTP/HTTPS 代理
    git config --global http.proxy http://127.0.0.1:端口号
    git config --global https.proxy http://127.0.0.1:端口号

    2. 如果你使用 SOCKS5 代理（例如某些 VPN 模式）
    git config --global http.proxy socks5://127.0.0.1:端口号
    git config --global https.proxy socks5://127.0.0.1:端口号