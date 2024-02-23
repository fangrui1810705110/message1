import requests

url = 'http://10.1.32.42:8080/accPortal/modbus/index'
data = {'button': 'refresh'}

response = requests.post(url, data=data)

# 检查响应状态码
if response.status_code == 200:
    print("按钮点击成功！")
else:
    print("按钮点击失败！")
