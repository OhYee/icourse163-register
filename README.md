# icourse163 中国大学mooc注册机

## 使用说明

### 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

需要安装selenium的Chrome相关工具,[下载地址](http://chromedriver.chromium.org/)
以及电脑上需要安装Chrome

由于没有设置无头浏览器，因此**需要图形界面支持**

### 配置信息

将`src/config/config.py.default`重命名为`src/config/config.py`并编辑数据，设置POP3服务器的地址、账号、密码，以及要自动关注的课程地址

### 运行

```bash
./run
```

## 依赖

- requests
- selenium
- Chrome Driver

## 接口说明

注册部分共有三个接口，分别用于发送验证码，验证验证码，注册账号

### 发送验证码

|字段名|备注||
|:---:|:---:|:---:|
|url|`http://www.icourses.cn/web//sword/portal/user/register/rg/getRegeditEmailCode`||
|method|POST||
|form-data|字段名|备注|
||email|要接受验证码的邮箱地址|

响应格式为json，其中`model`里的`data`存储的值为uuid后续有用

### 验证验证码


|字段名|备注||
|:---:|:---:|:---:|
|url|`http://www.icourses.cn/web//sword/portal/user/register/cm/validateCode`||
|method|POST||
|form-data|字段名|备注|
||id|邮箱地址|
||code|验证码|
||uuidToken|发送验证码时返回的数据|

响应格式为json


### 注册账号


|字段名|备注||
|:---:|:---:|:---:|
|url|`http://www.icourses.cn/web//sword/portal/user/register/rg/regedit`||
|method|POST||
|form-data|字段名|备注|
||name|用户名(不是邮箱)|
||pwd|用户密码|
||uuidToken|发送验证码时返回的数据|

响应格式为json

## 已知问题

1. selenium在输入账号登录、等到页面加载时，会由于速度问题导致无法正确按照流程操作。代码中已经使用`time.sleep()`尽可能避免这些问题
2. 注册账号过多时可能会被拉黑(待确认)
3. POP3连接服务器不稳定，采用每次重新进行连接的形式连接到POP3服务器