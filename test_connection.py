# 为复杂网络环境（如使用 VPN、代理或受限的企业内网）以及高安全限制的 Salesforce 实例（如 Agentforce 试用版）设计的自动化连接工具。
import os
import requests
import urllib3
from dotenv import load_dotenv
from simple_salesforce import Salesforce

# 屏蔽自签名证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 第一步：环境清理与初始化 (__init__)
        # 1. 加载环境变量
        # 2. 创建一个不受系统代理干扰的干净 Session（解决 SSLError 和 EOF Error）

class SalesforceClient: # 连接 Salesforce 的客户端类，封装了连接逻辑和查询方法
    def __init__(self): # 初始化方法，加载环境变量并创建干净的 Session
        load_dotenv() # 加载 .env 文件中的环境变量
        self.username = os.getenv('SF_USERNAME')
        self.password = os.getenv('SF_PASSWORD')
        self.token = os.getenv('SF_SECURITY_TOKEN')
        self.client_id = os.getenv('SF_CLIENT_ID')
        self.client_secret = os.getenv('SF_CLIENT_SECRET')
        self.login_url = os.getenv('SF_LOGIN_URL', 'https://login.salesforce.com')
        
        # 创建一个不受系统代理干扰的干净 Session
        self.session = self._create_clean_session()
        self.sf = None # Salesforce 实例，连接成功后会被初始化

    # 创建一个不受系统代理干扰的干净 Session，解决 SSLError 和 EOF Error
    def _create_clean_session(self):
        """创建一个不受系统代理干扰的干净 Session"""
        session = requests.Session()
        session.verify = False      # 解决 SSLError，相当于告诉 Python “即便对方的 SSL 证书看起来不完美，也请信任它”
        session.trust_env = False   # 强制忽略系统环境变量里的代理 (解决 EOF Error)，强制 Python 忽略你电脑操作系统里设置的任何全局代理（比如 VPN 开启时自动设下的系统代理）
        session.proxies = {'http': None, 'https': None} # 确保请求是物理直连到 Salesforce 官网，不经过任何中间转手。
        return session
    
    # 连接 Salesforce 的核心方法，Salesforce 组织禁用了传统的 SOAP 登录，所以采用“密码流 (Password Flow)” 这种现代化的置换方式。使用 OAuth2 密码流获取 Access Token 并初始化 Salesforce 实例，绕过 SOAP 限制。
    def connect(self): 
        """通过 OAuth2 密码流获取 Access Token 并初始化"""
        print(f"🛰️  正在接入 Salesforce (用户: {self.username})...") 
        

        # 第二步：OAuth 2.0 身份置换 (connect)

            # 1. 构造 payload: 代码并没有直接去登录，而是把 client_id、client_secret（Connected App 的身份证）、username 和 password + token（你的账号凭据）打包在一起。
            # 2. 向授权中心申请 Token: 它将这个包发给 .../services/oauth2/token 接口。这个接口会验证你的凭据，如果一切正确，它会返回一个 Access Token（访问令牌），这个 Token 就是你后续访问 Salesforce API 的“通行证”。
            # 通过这种方式，你就绕过了传统的 SOAP 登录限制，直接拿到一个可以用来访问 Salesforce 的 Token。之后你可以用这个 Token 来初始化 Salesforce 实例，进行各种 API 调用。
            # Salesforce 的 OAuth2 Token 端点 URL，通常是 https://login.salesforce.com/services/oauth2/token 或 https://test.salesforce.com/services/oauth2/token（取决于你连接的是生产环境还是沙箱环境）
        token_url = f"{self.login_url}/services/oauth2/token" 
        payload = { 
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': f"{self.password}{self.token}"
        }

        # 3. 获取临时通行证 (access_token):如果验证通过，Salesforce 会返回两个关键信息：access_token: 一个临时的、长串的密文通行证。instance_url: 告诉你你的数据在哪台服务器上（比如 https://ap24.salesforce.com）。
            # 发送 POST 请求获取 Access Token，并处理响应。使用 requests 库发送 POST 请求到 token_url，携带上面构造的 payload。设置 timeout=30 来避免请求长时间挂起。
            # 如果响应状态码是 200，说明授权成功，我们从响应中提取 instance_url 和 access_token，然后用它们来初始化 Salesforce 实例。
            # 这样我们就绕过了 SOAP 登录限制，直接拿到了一个可以用来访问 Salesforce API 的 Token。如果授权失败，我们打印错误信息并返回 None。如果在网络连接过程中发生异常（比如超时、连接错误等），我们捕获异常并打印错误信息。
        try:
            response = self.session.post(token_url, data=payload, timeout=30)
            # 标准的 REST API 调用：
            # 动作 (HTTP Verb): post。REST 规定，提交数据或执行登录这种“产生新资源”的操作要用 POST。
            # 地址 (Endpoint): token_url (即 .../services/oauth2/token)。REST 的特征之一就是每一个功能都有一个唯一的 URL 地址。
            # 数据格式: 你的 payload 字典最后会被转换成类似于网页表单的数据发出去，返回的 response.json() 则是典型的 REST 风格的 JSON 回复。
            if response.status_code == 200:
                auth_data = response.json()
                print(f"🎫 Access Token: {auth_data['access_token']}")
                print(f"📍 Instance URL: {auth_data['instance_url']}")
                # 4. 初始化 Salesforce 对象:使用拿到的 Token 手动初始化，绕过 SOAP 限制,这里没有传用户名密码，而是直接拎着刚拿到的“通行证”进场。
                self.sf = Salesforce(
                    instance_url=auth_data['instance_url'],
                    session_id=auth_data['access_token'],
                    session=self.session
                )
                print("✅ 连接成功！已绕过 SOAP 限制。")
                return self.sf
            else:
                print(f"❌ 授权失败: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"💥 网络连接异常: {e}")
            return None
    
    # 第三步：数据查询与输出 (query_org_info)
        # sf.query("SOQL语句"): 使用 Salesforce 的结构化查询语言获取数据。
        # results['records'][0]: simple-salesforce 会自动把服务器返回的 JSON 数据转成 Python 字典。
        # 测试方法：查询组织信息，验证连接是否成功，并展示一些基本的组织信息（如名称和类型）。如果连接成功，使用 Salesforce 实例执行一个简单的 SOQL 查询来获取组织的名称和类型，并打印出来。这个方法可以帮助确认连接是否真正建立，并且可以访问 Salesforce API。
    def query_org_info(self):
        """测试方法：查询组织信息"""
        if not self.sf:
            print("请先调用 connect()")
            return
        
        #REST 行为：查询数据，simple-salesforce 这个库在底层帮你翻译成了一个 REST 请求，它实际上向 Salesforce 发送了这样一个 HTTP 动作。
            # 方法: GET
            # 完整 URL: https://你的实例地址/services/data/v60.0/query/?q=SELECT+Name+FROM+Organization+LIMIT+1
            # 身份验证 (Header): 它悄悄在请求头里加了 Authorization: Bearer [你的Access Token]。
        results = self.sf.query("SELECT Name, OrganizationType FROM Organization LIMIT 1")
        org = results['records'][0]
        print(f"🏢 组织名称: {org['Name']}")
        print(f"🛠️  组织类型: {org['OrganizationType']}")

# --- 调用示例 ---
if __name__ == "__main__":
    client = SalesforceClient()
    sf_instance = client.connect()
    
    if sf_instance:
        client.query_org_info()
        # 之后可以直接使用 sf_instance 进行 CRUD 操作
        # 例如: sf_instance.Contact.create({'LastName': 'Test'})