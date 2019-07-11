from icourse.register import pop3_connect, register
from icourse.login import login, join, init_driver
import time

from config.config import *


def register_login_join(pop3, driver, username):
    username_with_email = "{}@{}".format(username, email_address)

    register(username, username_with_email, pop3)
    login(driver, username_with_email, username)
    join(driver, course_url)
    time.sleep(2)
    driver.delete_all_cookies()
    driver.get("https://www.icourse163.org/member/login.htm#/webLoginIndex")


if __name__ == "__main__":
    try:
        driver = init_driver()

        for i in range(begin, end):
            username = "icourse%03d" % i
            pop3 = pop3_connect(email_pop3_url, email_pop3_ursename,
                                email_pop3_password)
            print("已连接到pop3服务器")
            register_login_join(pop3, driver, username)
    finally:
        driver.close()
