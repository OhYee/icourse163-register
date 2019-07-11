import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login(driver, username, password):
    print("登入", username, password)

    driver.get("https://www.icourse163.org/member/login.htm#/webLoginIndex")

    # # 登录按钮
    # button = driver.find_element_by_class_name(
    #     "course-enroll-info_course-enroll_buttons_enroll-btn")
    # button.click()

    # 使用icourse账号登录
    buttons = driver.find_elements_by_class_name("last-login-holder")
    buttons[2].click()

    # 输入账号密码
    inputs = driver.find_elements_by_class_name("ux-input_addon_shrinkage")
    time.sleep(3)
    inputs[0].send_keys(username)
    time.sleep(3)
    inputs[1].send_keys(password)
    time.sleep(3)

    # 点击登录按钮
    submit = driver.find_element_by_class_name(
        "submit-button")
    submit.click()


def join(driver, url):
    print("加入课程", url)

    driver.get(url)

    try:
        # 暂不绑定
        time.sleep(2)
        button = driver.find_element_by_class_name(
            "ignore-bind")
        button.click()
        time.sleep(2)
    except:
        pass

    # 加入课程
    button = driver.find_element_by_class_name(
        "course-enroll-info_course-enroll_buttons_enroll-btn")
    button.click()


def init_driver():
    driver = webdriver.Chrome("chromedriver.exe")
    return driver
