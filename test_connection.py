import os
from dotenv import load_dotenv
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed

# 加载 .env 环境变量
load_dotenv()
# load_dotenv() 之后添加
print(f"调试：用户名是 {os.getenv('SF_USERNAME')}")

def test_sf_connection():
    # 从环境变量获取配置
    username = os.getenv('SF_USERNAME')
    password = os.getenv('SF_PASSWORD')
    token = os.getenv('SF_SECURITY_TOKEN')

    print("🚀 正在尝试连接 Salesforce...")

    try:
        # 建立连接
        # 对于 Developer Edition，domain 设置为 'test' 通常用于 Sandbox，
        # 默认不填则是连接到 Login.salesforce.com (生产/开发者版)
        sf = Salesforce(
            username=username,
            password=password,
            security_token=token,
            domain='login'
        )

        # 执行一个简单的 SOQL 查询来验证
        org_info = sf.query("SELECT Name FROM Organization LIMIT 1")
        org_name = org_info['records'][0]['Name']

        print("✅ 连接成功！")
        print(f"🏢 组织名称: {org_name}")
        print(f"👤 登录用户: {username}")

    except SalesforceAuthenticationFailed:
        print("❌ 连接失败：身份验证错误，请检查用户名、密码或 Token。")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    test_sf_connection()