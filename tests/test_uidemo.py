# 这个测试用例演示了如何结合 Playwright 和 Salesforce API 来进行端到端的 UI 测试。
# 场景：通过 API 创建一个测试门店，然后使用 Playwright 自动化浏览器访问 Salesforce UI，验证创建的门店信息是否正确显示在页面上。
# 1. 定义一个 pytest fixture 来准备测试数据（通过 API 创建一个门店，并获取它的 ID 和 URL）
# 2. 编写一个测试函数，使用 Playwright 的 Page 对象来模拟用户操作：访问登录页、输入用户名和密码、点击登录按钮、等待页面加载完成
# 3. 直接通过 URL 跳转到我们 API 创建的门店详情页
# 4. 使用 Playwright 的断言功能来验证页面上是否正确显示了我们创建的门店名称
# 5. 最后打印验证结果，确认整个流程是否成功
# 注意：Salesforce 的登录通常会有验证码，如果你的测试环境开启了 MFA，建议在测试环境关闭 MFA，或者手动登录一次保持 Session，这样 Playwright 就可以直接访问页面而不需要处理验证码。

import pytest
from playwright.sync_api import Page, expect

# 使用刚才生成的 auth.json 启动浏览器上下文
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": "auth.json"
    }

def test_go_to_salesforce_home(page: Page):
    # 这里直接写 Salesforce 实例地址（或者登录后的主页地址）
    # 比如：https://xxxx.lightning.force.com/lightning/page/home
    home_url = "ehttps://orgfarm-e632a316c7-dev-ed.develop.lightning.force.com/lightning/page/hom"
    
    print("\n🚀 正在利用已保存的状态自动进入...")
    page.goto(home_url)
    print(f"📍 当前页面实际 URL: {page.url}") 
    # 如果打印出来还是包含 "login.salesforce.com"，说明登录失效了，需要重新跑 save_auth.py

    # 1. 验证是否跳过了登录页，直接看到了主页的内容
    # 我们检查左上角的“App Launcher”（九宫格按钮）是否存在
    app_launcher = page.locator("div.slds-icon-waffle")
    
    # 期待它在 10 秒内出现
    expect(app_launcher).to_be_visible(timeout=10000)
    
    print("🎉 成功！已绕过登录，直接进入 Salesforce 主页面。")
    
    # 截图一张作为证据
    page.screenshot(path="sf_home_page.png")

# 运行命令: pytest test_sf_home.py --headed -s