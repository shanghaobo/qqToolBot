from django.test import TestCase
import requests as r
import base64

# Create your tests here.

# menu_list={
#     '1':'短连接生成',
#     '2':'二维码生成',
#     '3':'图片转文字'
# }
#
# for key,value in menu_list.items():
#     print(key,value)


# fun_list={
#     '01#':'shortUrl',
#     '02#':'codeMake'
# }
#
# def shortUrl(**info):
#     print(info)
#
# globals().get(fun_list['05#'])(a=1,b=2)


url='http://ai.baidu.com/aidemo'
data={
    'type':'tns',
    'spd':'5',
    'pit':'5',
    'vol':'5',
    'per':'0',
    'tex':'怎么大风越狠，我心越荡'
}
headers={
    'Content-Type':'application/x-www-form-urlencoded',
    'Referer':'http://ai.baidu.com/tech/speech/tts'
}
cookies={
    'BAIDUID':'5F8B3EA360A7ABB25094DFB846D853AF:FG=1'
}

res=r.post(url,data=data,headers=headers,cookies=cookies)
jsondata=res.json()
base64_data=jsondata['data'].replace('data:audio/x-mpeg;base64,','')
print(base64_data)
s=base64.b64decode(base64_data)
print(s)
file_url='E:/test.mp3'
with open(file_url,'wb+') as mp3:
    mp3.write(s)
