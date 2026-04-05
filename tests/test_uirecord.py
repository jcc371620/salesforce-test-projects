# record了一下登录和导航的过程，主要是为了拿到登录状态（Cookies 和 LocalStorage），保存到 auth.json 文件中。这样后续的测试就可以直接加载这个文件来恢复登录状态，避免每次都需要手动输入验证码。

import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.get_by_role("textbox", name="用户名").click()
    page.get_by_role("textbox", name="用户名").fill("jcc371620.23e8690d49fa@agentforce.com")
    page.get_by_role("textbox", name="密码").click()
    page.get_by_role("textbox", name="密码").fill("test12345")
    page.get_by_role("checkbox", name="记住我").check()
    page.get_by_role("button", name="登录").click()
    page.goto("https://orgfarm-e632a316c7-dev-ed.develop.my.salesforce.com/_ui/identity/verification/method/EmailVerificationFinishUi/e?vcsrf=IZXuTuuA--KM8DYjJQTzLMrtebUdANVRwTrnHbmcwPsaPOaUefDH-0pBLjoVL1vjZH-ybZd0j5Nl-VajLIOPG_HFtEhklfU9_syC-wBDatLM9Q4H-FIKQTz8X-xstG9cNO-OlVeGb0h3CEG15AOAHDrNfhIcEoTIdUdV3bp7UuLlKOr6nEuySY0pKGftFWrSwVwXQpSYpVB659QNC2Jb-TR8B_4e1YXGCgqnbozpOxyHPUXBOVx0-SCJ-sWvDDi1oAlLMKm9Sc-UqNSkKMNjFMyD-wPazpEsRdtTmEfKEQ1QcERCj8wvGZZYHoJbUFGtzO5F2KQ2kNkX2ntT88cN5mZpQaWyqljDj_Ex-Crgecnl4NlHCItxAd0tJgjjIX4rVw_3ZYYxrKaJN-liRHU038MT095qhMe87wFednZ1uIgT7R4TMQf2ighM8TDNtZwfUBuWyLELuwQOO4_CfAXNrynecOvr-einz8O3DYtukgEeqK18EjJW_V1GvzQK4VUj3JPDAjavsWbUhMmfF5Qs_wR0MJc9roPsuzJIVU7H5fNMycv4qGkYu1JFKwfG8c0z-_CMtakuRqYMfqUKaHlhW9vTnwiKSH4Lcfp2UDaBDfK_FCuqjsO-IwIXGJHjJFnNTvxNy16YvFCYBzfSw_t-nddUSVXDhrQlVyMXUMu3vIo%3D&vpol=ic&vflid=0&vfgrp=2058063547&retURL=%2Fsecur%2Ffrontdoor.jsp%3Fallp%3D1%26cshc%3DK00002zom0GK00000McFFu%26apv%3D1%26display%3Dpage%26ucs%3D1")
    page.get_by_role("textbox", name="Verification Code").click()
    page.get_by_role("textbox", name="Verification Code").fill("245463")
    page.get_by_role("button", name="Verify").click()
    page.goto("https://orgfarm-e632a316c7-dev-ed.develop.lightning.force.com/lightning/page/home")
    page.get_by_role("button", name="App Launcher").click()
    page.get_by_role("button", name="App Launcher").click()
    page.get_by_role("combobox", name="Search apps and items...").click()
    page.get_by_role("combobox", name="Search apps and items...").fill("acc")
    page.get_by_role("option", name="Accounts").click()
    page.get_by_role("button", name="New").click()
    page.get_by_role("textbox", name="Account Name").click()
    page.get_by_role("textbox", name="Account Name").fill("acc")
    page.get_by_role("button", name="Save & New").click()
    page.get_by_role("button", name="Cancel and close").click()
    page.locator(".center.oneCenterStage.lafSinglePaneWindowManager").click()
