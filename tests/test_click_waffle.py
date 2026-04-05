# 这个测试脚本的目的是验证在 Salesforce Lightning 主页上点击九宫格（App Launcher）是否能够成功弹出菜单。这个测试主要关注 UI 元素的交互，确保九宫格按钮能够被正确定位和点击。
# 主要步骤包括：
# 1. 使用 Playwright 的 Page 对象访问 Salesforce Lightning 主页。
# 2. 定位九宫格按钮（通常是一个带有特定 class 的 div 或 button 元素）。
# 3. 等待九宫格按钮可见并且没有被遮挡，然后执行点击操作。
# 4. 使用 page.pause() 暂停测试，允许测试人员手动观察点击后的效果，确认菜单是否成功弹出。

import pytest
from playwright.sync_api import Page, expect

# 1. 注入登录状态 (确保 auth.json 已存在)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args, 
        "storage_state": "auth.json"
    }

def test_only_click_app_launcher(page: Page):
    # --- 配置区域 ---
    # 请替换为你登录后的实际 Lightning 主页 URL
    home_url = "https://orgfarm-e632a316c7-dev-ed.develop.lightning.force.com/lightning/page/home" 
    
    print(f"\n🚀 正在前往主页...")
    
    # --- 步骤 1: 访问主页 ---
    # 去掉 networkidle，增加超时到 60 秒，防止 Salesforce 加载太慢报错
    page.goto(home_url, wait_until="domcontentloaded", timeout=60000)
    
    # --- 步骤 2: 等待并点击九宫格 ---
    print("🖱️ 正在定位九宫格 (App Launcher)...")
    
    # 使用更稳健的定位器：九宫格通常是一个 button 或者是带特定 class 的 div
    # Salesforce 官方标准定位是这个 class
    waffle_button = page.locator("div.slds-icon-waffle")
    
    # 显式等待：确保它在页面上可见且没有被遮挡
    expect(waffle_button).to_be_visible(timeout=20000)
    
    # 执行点击
    waffle_button.click()
    print("✅ 点击成功！")

    # --- 步骤 3: 暂停观察 ---
    # 这一行会让浏览器停住，并弹出调试窗口，你可以亲眼看到菜单是否弹出来了
    page.pause()

# 运行命令: pytest tests/test_click_waffle.py --headed -s