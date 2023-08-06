from hahaha_utils.web_request import WebRequest

wr = WebRequest()

resp = wr.get('https://www.douyin.com')
print(resp.text)