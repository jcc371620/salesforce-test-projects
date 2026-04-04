# 测试步骤定义：Contact 相关的 API 和 UI 验证
import os 
from simple_salesforce import Salesforce
from pytest_bdd import scenario, given, when, then
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

load_dotenv()

@scenario('../features/contact.feature', 'Create a contact via API and verify in Salesforce UI')
def test_contact_e2e():
    """BDD 场景入口"""
    pass

# --- Step 1: 使用 simple-salesforce 执行 API 操作 (相当于 SQL 写入) ---
@given('I create a contact named "Gemini_Test_User" via REST API', target_fixture="contact_info")
def create_contact_api():
    # 建立连接（它会自动处理登录获取 Token）
    sf = Salesforce(
        username=os.getenv('SF_USERNAME'),
        password=os.getenv('SF_PASSWORD'),
        security_token=os.getenv('SF_SECURITY_TOKEN'),
        domain='test' if 'sandbox' in os.getenv('SF_INST_URL') else 'login'
    )
    
    last_name = "Gemini_Test_User"
    
    # 逻辑 A: 先用 SOQL (SQL) 检查用户是否存在，存在则先删除 (保持测试幂等性)
    query_result = sf.query(f"SELECT Id FROM Contact WHERE LastName = '{last_name}'")
    for record in query_result['records']:
        sf.Contact.delete(record['Id'])
        print(f"已清理旧数据: {record['Id']}")

    # 逻辑 B: 创建新联系人
    result = sf.Contact.create({'LastName': last_name, 'Company': 'AI_Test_Lab'})
    print(f"API 创建成功, ID: {result['id']}")
    
    return {"LastName": last_name, "Id": result['id']}

# --- Step 2: 使用 Playwright 执行 UI 操作 ---
@when('I login to Salesforce and search for "Gemini_Test_User"')
def login_and_search(page: Page):
    # 登录 UI
    page.goto(os.getenv('SF_INST_URL'))
    page.fill("#username", os.getenv('SF_USERNAME'))
    page.fill("#password", os.getenv('SF_PASSWORD'))
    page.click("#Login")
    
    # 直接跳转到该 Contact 的列表页，效率更高
    contact_list_url = f"{os.getenv('SF_INST_URL')}/lightning/o/Contact/list"
    page.goto(contact_list_url)
    page.wait_for_load_state("networkidle")

# --- Step 3: 断言验证 ---
@then('I should see the contact details on the screen')
def verify_contact_ui(page: Page, contact_info):
    # 在搜索框或列表中验证名字
    target_name = contact_info["LastName"]
    
    # Playwright 强大的定位器，会自动等待元素出现
    expect(page.get_by_role("link", name=target_name)).to_be_visible()
    print(f"UI 验证成功: 找到了 {target_name}")