import re
from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 和第一个测试保持一致：直接进入新建页面
    page.goto(f"{live_server}/cars/new")

    # 创建 Honda Civic, 2022
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    # 等待详情页加载完成，标题出现
    expect(page.get_by_role("heading", name="Honda Civic")).to_be_visible()

    # 点击编辑链接
    page.get_by_role("link", name="Edit car").click()

    # 修改为 Accord + 2023
    model_input = page.get_by_label("Model", exact=True)
    model_input.fill("Accord")
    year_input = page.get_by_label("Year", exact=True)
    year_input.fill("2023")

    # 保存修改
    page.get_by_role("button", name="Save changes").click()

    # 断言详情页标题更新
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 刷新页面
    page.reload()

    # 刷新后校验数据持久化
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
