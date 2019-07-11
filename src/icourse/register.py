import requests
from requests.adapters import HTTPAdapter
import base64
import re
import poplib
import time

def format_email(data):
    '''格式化POP3邮件内容'''
    res = {
        "state": data[0],
        "length": data[2],
    }
    last_form = ""
    for line_bytes in data[1]:
        line = line_bytes.decode("utf-8")

        matches = re.findall(r'^(.*): (.*)$', line)
        if matches:
            last_form = matches[0][0]
            res[matches[0][0]] = matches[0][1]
        elif len(line) == 0:
            continue
        elif line[0] == "\t":
            res[last_form] = res[last_form] + line[1:]
        else:
            if "body" in res:
                res["body"] += line
            else:
                res["body"] = line
    return res


def pop3_connect(url, username, password):
    pop3 = poplib.POP3_SSL(url)
    pop3.user(username)
    pop3.pass_(password)
    return pop3


def get_valid_code(pop3, username_with_email):

    num = pop3.stat()[0]
    for i in range(num, 0, -1):
        email = format_email(pop3.retr(i))
        if email["Content-Transfer-Encoding"] == "base64" and email["To"] == username_with_email:
            body = base64.b64decode(email["body"]).decode("utf-8")
            codes = re.findall(r"\d{4}", body)
            if codes:
                return codes[0]
    return 0


def register(username, username_with_email, pop3):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=10))
    session.mount('https://', HTTPAdapter(max_retries=10))

    # 发送验证邮件
    valid_email_rep = requests.post(
        "http://www.icourses.cn/web//sword/portal/user/register/rg/getRegeditEmailCode",
        data={
            "email": username_with_email
        },
        timeout=(10, 10)
    )
    valid_email_json = valid_email_rep.json()
    uuid = valid_email_json["model"]["data"]
    if username == "":
        uuid = "9308fabe7c8b416a94d1ca8d28f4d165"
    print("{} {} {}".format(username_with_email,
                            valid_email_json["model"]["message"], uuid))

    if valid_email_json["model"]["message"] == "账号已存在":
        return

    retry = 5
    code = 0
    while retry > 0:
        try:
            # 获取验证码
            time.sleep(5)
            code = get_valid_code(pop3, username_with_email)
            print("验证码 {}".format(code))

            # 验证验证码
            valid_code_rep = requests.post(
                "http://www.icourses.cn/web//sword/portal/user/register/cm/validateCode",
                data={
                    "id": username_with_email,
                    "code": code,
                    "uuidToken": uuid,
                },
                timeout=(10, 10)
            )
            valid_code_json = valid_code_rep.json()
            print(valid_code_json["model"]["message"])  # 验证成功
            if valid_code_json["model"]["message"] != "验证成功":
                raise Exception()

            # 注册账号
            register_rep = requests.post(
                "http://www.icourses.cn/web//sword/portal/user/register/rg/regedit",
                data={
                    "pwd": username,
                    "name": username+"o",
                    "uuidToken": uuid,
                },
                timeout=(10, 10)
            )
            register_json = register_rep.json()
            print(register_json["model"]["message"])  # 成功
            if register_json["model"]["message"] != "成功":
                raise Exception()

            return
        except Exception as e:
            retry -= 1
            print("错误,重新读入验证码", e)
    raise Exception()
