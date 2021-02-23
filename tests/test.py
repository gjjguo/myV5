#coding:utf-8
''''''
# import re
# my_string='{"moblie_phone":"#investor_phone#"}'
# pattern='#(.*?)#'
# result=re.search(pattern=pattern,string=my_string)
# print(result.group())
# print(result.group(1))
import requests
data={"pageIndex":1,"pageSize": 10}
res=requests.get(url='http://api.lemonban.com/futureloan/loans',
             params=data)
print(res)
result=res.json()
print(result)
