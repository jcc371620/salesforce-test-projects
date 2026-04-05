# 这个测试脚本的目的是验证在 Salesforce Lightning 主页上使用搜索功能查找 "Accounts" 并成功导航到 Accounts 列表页的流程。这个测试主要关注 UI 元素的交互和页面导航，确保用户能够通过搜索快速访问 Accounts 页面。
# 主要步骤包括：
# 1. 使用 Playwright 的 Page 对象访问 Salesforce Lightning 主页。
# 2. 点击九宫格（App Launcher）图标，打开应用菜单。
# 3. 在搜索框中输入 "accou"，触发搜索功能。
# 4. 从搜索结果中找到 "Accounts" 选项并点击它。
# 5. 验证是否成功导航到 Accounts 列表页（通常 URL 会包含 /lightning/o/Account/list）。
# 6. 最后使用 page.pause() 暂停测试，允许测试人员手动观察最终结果，确认是否成功跳转到 Accounts 列表页。

import pytest
from playwright.sync_api import Page, expect

# 注入登录状态 (确保你的项目根目录下已有有效的 auth.json)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args, 
        "storage_state": "auth.json",
        "viewport": {"width": 1280, "height": 800} # 设置固定分辨率增加稳定性
    }

def test_search_and_go_to_accounts(page: Page):
    # 【⚠️ 重要】请把下面这个网址换成你登录后浏览器地址栏里的真实域名
    # 格式：https://xxxxx.lightning.force.com/lightning/page/home
    home_url = "https://orgfarm-e632a316c7-dev-ed.develop.lightning.force.com/lightning/page/home" 

    print(f"\n🚀 启动自动化测试，尝试进入: {home_url}")

    # 1. 访问主页
    # 使用 wait_until="commit" 绕过 networkidle 超时错误
    try:
        page.goto(home_url, wait_until="commit", timeout=60000)
    except Exception as e:
        print(f"⚠️ 初始加载异常，尝试继续等待元素: {e}")

    # 2. 检查是否被踢回了登录页
    if "login.salesforce.com" in page.url:
        pytest.fail("❌ 登录失效！请重新运行 save_auth.py 更新 auth.json")

    # 3. 点击九宫格 (App Launcher)
    print("🖱️ 正在点开九宫格...")
    waffle = page.locator("div.slds-icon-waffle")
    # 确保图标渲染出来后再点
    expect(waffle).to_be_visible(timeout=30000)
    waffle.click()

    # 4. 在搜索框输入 "accou"
    print("⌨️ 正在搜索 'accou'...")
    # Salesforce 弹窗有动画，稍微等一下输入框出现
    search_input = page.get_by_placeholder("Search apps and items...")
    expect(search_input).to_be_visible(timeout=15000)
    search_input.fill("accou")
    
    # 稍微停顿，让搜索结果列表加载出来
    page.wait_for_timeout(1000)

    # 5. 点击搜索结果中的 "Accounts"
    print("🔍 正在点击搜索结果中的 Accounts...")
    # .first 确保点到的是第一个匹配项，规避可能出现的类似名称
    accounts_option = page.get_by_role("option", name="Accounts").first
    expect(accounts_option).to_be_visible(timeout=10000)
    accounts_option.click()

    # 6. 验证是否成功进入 Accounts 列表页
    print("✅ 正在验证跳转结果...")
    # 只要 URL 包含 Account/list 就算成功
    page.wait_for_url("**/lightning/o/Account/list**", timeout=20000)
    page.pause()  # 观察结果，确认是否成功跳转到 Accounts 列表页
    # 打印最终到达的 URL 确认战果
    print(f"🎉 任务完成！当前页面: {page.url}")
    
    # 截图保存
    page.screenshot(path="success_navigation.png")

    

# 运行命令: pytest tests/test_sf_search_acc.py --headed -s