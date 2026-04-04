import os
import requests
import urllib3
from dotenv import load_dotenv
from simple_salesforce import Salesforce

# 屏蔽自签名证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SalesforceClient:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('SF_USERNAME')
        self.password = os.getenv('SF_PASSWORD')
        self.token = os.getenv('SF_SECURITY_TOKEN')
        self.client_id = os.getenv('SF_CLIENT_ID')
        self.client_secret = os.getenv('SF_CLIENT_SECRET')
        self.login_url = os.getenv('SF_LOGIN_URL', 'https://login.salesforce.com')
        
        self.session = self._create_clean_session()
        self.sf = None

    def _create_clean_session(self):
        """创建一个不受系统代理干扰的干净 Session"""
        session = requests.Session()
        session.verify = False      # 解决 SSLError
        session.trust_env = False   # 强制忽略系统环境变量里的代理 (解决 EOF Error)
        session.proxies = {'http': None, 'https': None} # 强制直连
        return session

    def connect(self):
        """通过 OAuth2 密码流获取 Access Token 并初始化"""
        print(f"🛰️  正在接入 Salesforce (用户: {self.username})...")
        
        token_url = f"{self.login_url}/services/oauth2/token"
        payload = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': f"{self.password}{self.token}"
        }

        try:
            response = self.session.post(token_url, data=payload, timeout=30)
            
            if response.status_code == 200:
                auth_data = response.json()
                # 使用拿到的 Token 手动初始化，绕过 SOAP 限制
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

    def query_org_info(self):
        """测试方法：查询组织信息"""
        if not self.sf:
            print("请先调用 connect()")
            return
        
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
        # 之后你可以直接使用 sf_instance 进行 CRUD 操作
        # 例如: sf_instance.Contact.create({'LastName': 'Test'})