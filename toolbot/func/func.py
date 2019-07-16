import requests as r
import random
import qrcode
from .handle import sendPrivateMsg,orc_url,updateStatus,word_to_voice,shell_screen
import time

#短连接转换
def shortUrl(**info):
    # text=info['msg'][3:]
    if info['status']=='0':
        updateStatus(info['qq'],'01')
        reply = '请回您要转换的链接'
        sendPrivateMsg(info['qq'], reply)
    else:
        updateStatus(info['qq'], '0')
        if info['msg'].find('CQ:share')!=-1:
            i1 = info['msg'].find('url=')
            i2 = info['msg'].find(']', i1)
            url = info['msg'][i1 + 4:i2]
        url = url.strip().replace('\n', '')
        print('url=%s'%url)
        res = r.get('http://api.t.sina.com.cn/short_url/shorten.json?source=2815391962&url_long=%s' % url)
        res = res.json()
        try:
            reply = res[0]['url_short']
        except:
            reply = '回复的链接有误'
        sendPrivateMsg(info['qq'], reply)


#二维码生成
def codeMake(**info):
    # text = info['msg'][3:]
    if info['status']=='0':
        updateStatus(info['qq'], '02')
        reply = '请回复您要生成的二维码信息'
        sendPrivateMsg(info['qq'], reply)
    else:
        updateStatus(info['qq'], '0')
        temp = str(random.randint(10000, 100000))
        file_url = '/root/coolq_tool/data/image/%s.jpg' % temp
        img = qrcode.make(info['msg'])
        img.save(file_url)
        reply = '[CQ:image,file=%s.jpg]' % temp
        sendPrivateMsg(info['qq'], reply)


#图片转文字
def ocr(**info):
    if info['status']=='0':
        updateStatus(info['qq'], '03')
        reply='请发送您要识别的图片'
        sendPrivateMsg(info['qq'],reply)
    else:
        updateStatus(info['qq'], '0')
        img=info['msg']
        i1=img.find('url=')
        i2=img.find(';',i1)
        url=img[i1+4:i2]
        print('url=%s'%url)
        txt=orc_url(url)
        if txt:
            reply=txt
        else:
            reply='识别失败,只支持PNG,JPG,JPEG,BMP格式,图片大小不超过4M且长边不大于4096像素'
        sendPrivateMsg(info['qq'], reply)


def wordToImg(**info):
    sendPrivateMsg(info['qq'],'正在开发...')



#文字转语音
def wordToVoice(**info):
    if info['status']=='0':
        updateStatus(info['qq'], '05')
        reply = '请回复您要转化的文字'
        sendPrivateMsg(info['qq'], reply)
    else:
        updateStatus(info['qq'], '0')
        filename=word_to_voice(info['msg'])
        if filename:
            reply='[CQ:record,file=%s,magic=false]'%filename
        else:
            reply='转化失败'
        sendPrivateMsg(info['qq'],reply)

#带壳截图
def shellScreen(**info):
    if info['status']=='0':
        updateStatus(info['qq'], '06')
        reply = '请发送原来的图片'
        sendPrivateMsg(info['qq'], reply)
    else:
        updateStatus(info['qq'], '0')
        img = info['msg']
        i1 = img.find('url=')
        i2 = img.find(';', i1)
        url = img[i1 + 4:i2]
        print('url=%s' % url)
        newimg=shell_screen(url)
        if newimg:
            reply='[CQ:image,file=%s]'%newimg
        else:
            reply='转化失败'
        sendPrivateMsg(info['qq'],reply)