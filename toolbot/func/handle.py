from .mybot import *
global bot
import requests as r
from toolbot.models import *
import base64
import random
from PIL import Image
import io

bot=CQ()

#更新用户状态
def updateStatus(qq, status):
    res = UserStatus.objects.filter(qq=qq)
    if res.count() == 0:
        UserStatus.objects.create(qq=qq, status=status)
    else:
        res.update(qq=qq, status=status)


#获取机器人QQ
def getBotQQ():
    botQQ=None
    try:
        botQQ = bot.get_login_info()['user_id']
        print('机器人QQ:%s' % botQQ)
    except:
        print('获取机器人信息错误')
    finally:
        return botQQ

#发送私聊消息
def sendPrivateMsg(qq,msg):
    return bot.send_private_msg(user_id=qq, message=msg, auto_escape=False)

#发送赞
def sendLike(qq,times):
    return bot.send_like(user_id=qq, times=10)

'''
flag	string	-	加群请求的 flag（需从上报的数据中获得）
sub_type 或 type	string	-	add 或 invite，请求类型（需要和上报消息中的 sub_type 字段相符）
approve	boolean	true	是否同意请求／邀请
reason	string	空	拒绝理由（仅在拒绝时有效）
'''
def setGroupAddRequest(flag,type,approve,reason):
    return bot.set_group_add_request(flag=flag,type=type,approve=approve,reason=reason)


'''
flag	string	-	加好友请求的 flag（需从上报的数据中获得）
approve	boolean	true	是否同意请求
remark	string	空	添加后的好友备注（仅在同意时有效）
'''
def setFriendAddRequest(flag,approve,remark):
    return bot.set_friend_add_request(flag=flag,approve=approve,remark=remark)


#图片转文字 可支持PNG、JPG、JPEG、BMP，图片大小不超过4M，长边不大于4096像素
def orc_url(url):
    data = {}
    headers = {}
    data['type'] = 'commontext'
    data['image_url'] = url
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = 'http://ai.baidu.com/tech/ocr/general?castk=LTE%3D&qq-pf-to=pcqq.c2c'
    cookies = {'BAIDUID': '5F8B3EA360A7ABB25094DFB846D853AF:FG=1'}
    res = r.post(url='http://ai.baidu.com/aidemo', data=data, headers=headers, cookies=cookies)
    try:
        jsondata = res.json()
    except:
        return False
    print(jsondata)
    try:
        if jsondata['msg']=='success':
            txt=''
            words_result=jsondata['data']['words_result']
            for word in words_result:
                txt+=word['words']+'\n'
            print(txt)
            return txt
    except:
        return False


def word_to_voice(txt):
    try:
        url = 'http://ai.baidu.com/aidemo'
        data = {
            'type': 'tns',
            'spd': '5',
            'pit': '5',
            'vol': '5',
            'per': '0',
            'tex': txt
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://ai.baidu.com/tech/speech/tts'
        }
        cookies = {
            'BAIDUID': '5F8B3EA360A7ABB25094DFB846D853AF:FG=1'
        }

        res = r.post(url, data=data, headers=headers, cookies=cookies)
        jsondata = res.json()
        base64_data = jsondata['data'].replace('data:audio/x-mpeg;base64,', '')
        # print(base64_data)
        s = base64.b64decode(base64_data)
        # print(s)
        temp = str(random.randint(10000, 100000))
        filename = temp + '.mp3'
        file_url = '/root/coolq_tool/data/record/%s' % filename
        with open(file_url, 'wb+') as mp3:
            mp3.write(s)
        return filename
    except:
        print('error')
        return False


def shell_screen(imgurl):
    try:
        res = r.get(imgurl).content
        ioImg = io.BytesIO(res)
        img = Image.open(ioImg)  # 要转化的图片
        img_temp = Image.open('/root/django/qqToolBot/qqToolBot/static/images/template.png')
        x, y = img_temp.size
        # print(img)
        # print(x,y)

        newWidth, newHeight = 728, 1490
        img = img.resize((newWidth, newHeight))
        copyimg = img.crop((0, 0, newWidth, newHeight))
        img_temp.paste(copyimg, (176, 339))

        temp = str(random.randint(10000, 100000))
        filename = temp + '.png'
        file_url = '/root/coolq_tool/data/image/%s' % filename
        img_temp.save(file_url)
        img.close()
        img_temp.close()
        return filename
    except:
        return False