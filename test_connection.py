import os
import pytest
import requests
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量读取配置
USERNAME = os.getenv("SF_USERNAME")
PASSWORD = os.getenv("SF_PASSWORD")
SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

# 密码 + token 拼接
FULL_PASSWORD = f"{PASSWORD}{SECURITY_TOKEN}"


@pytest.fixture(scope="session")
def sf_connection():
    """连接Salesforce并返回instance_url和access_token"""
    login_url = "https://login.salesforce.com/services/oauth2/token"
    
    payload = {
        "grant_type": "password",
        "client_id": "PythonConnectionTest",
        "client_secret": "",
        "username": USERNAME,
        "password": FULL_PASSWORD
    }
    
    response = requests.post(login_url, data=payload, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    return data["instance_url"], data["access_token"]


def test_connection_success(sf_connection):
    """测试连接是否成功，成功则打印信息"""
    instance_url, access_token = sf_connection
    
    # 打印成功信息
    print(f"\n✅ Salesforce连接成功！")
    print(f"   Instance URL: {instance_url}")
    print(f"   Access Token: {access_token[:30]}...")
    
    # 可选：验证一下token确实能用，再打印一条确认
    query_url = f"{instance_url}/services/data/v58.0/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(query_url, headers=headers, params={"q": "SELECT Id FROM Account LIMIT 1"})
    
    if resp.status_code == 200:
        print("   ✅ Token验证通过，可以正常查询数据")
    else:
        print(f"   ⚠️ Token验证失败: {resp.status_code}")
    
    # 断言，让pytest知道测试通过
    assert resp.status_code == 200