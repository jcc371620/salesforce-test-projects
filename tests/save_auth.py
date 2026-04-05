# 一个专门的登录脚本，你手动输入用户名、密码和验证码。Playwright 会把你的“登录成功凭证”（Cookies 和 LocalStorage）存进一个名为 auth.json 的文件。这个脚本的目的是使用 Playwright 自动化登录 Salesforce，并将登录状态保存到一个 JSON 文件中。这样，在后续的测试或脚本中，我们就可以直接加载这个 JSON 文件来恢复登录状态，避免每次都需要手动输入验证码。
# 主要步骤包括：
# 1. 使用 Playwright 启动一个浏览器实例，并打开 Salesforce 的登录页面。
# 2. 等待用户在浏览器中完成登录操作（包括输入用户名、密码和验证码）。
# 3. 登录成功后，使用 Playwright 的 storage_state 功能将当前的登录状态保存到一个名为 auth.json 的文件中。
# 4. 以后在需要登录状态的测试或脚本中，可以直接加载这个 auth.json 文件来恢复登录状态，从而实现自动化登录。

from playwright.sync_api import sync_playwright

def save_salesforce_auth():
    with sync_playwright() as p:
        # headless=False 必须看得见，否则你没法手动点验证码
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. 访问登录页面
        page.goto("https://login.salesforce.com")
        print("💡 请在浏览器中完成登录（包括验证码）...")

        # 2. 这里的代码会停下，直到你看到主页上的某个元素（比如全局搜索框）
        # 或者你可以简单地设置一个超长等待，让你有时间操作
        # page.wait_for_selector("button.slds-button_last", timeout=60000) 
        
        print("🛠️ 已开启暂停模式。请在浏览器中完成所有登录步骤...")
                # 程序会在这里停住，直到你在小窗口点“继续”
        page.pause()

        # 3. 登录成功后，保存状态到文件
        context.storage_state(path="auth.json")
        print("✅ 登录状态已保存到 auth.json，以后可以自动登录了！")
        
        browser.close()

if __name__ == "__main__":
    save_salesforce_auth()