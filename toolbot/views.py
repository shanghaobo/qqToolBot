from django.shortcuts import render,HttpResponse
import json
from .func.handle import sendPrivateMsg,setGroupAddRequest,setFriendAddRequest
from .func.func import *
from .models import *





# Create your views here.
def index(request):
    data=request.body
    data=str(data,encoding='utf-8')
    data=json.loads(data)
    print('data=',data)
    try:
        sub_type = data['sub_type']
    except:
        sub_type=None
    if sub_type=='friend':#私有消息
        try:
            info={}
            info['botqq']=data['self_id']#机器人QQ
            info['qq']=data['sender']['user_id']#QQ
            info['msg']=data['message']#消息内容
            info['time']=data['time']#时间
            print('info:%s'%info)
        except:
            print('获取消息info错误')
        else:
            menu(**info)
            keyHandle(**info)
    elif sub_type=='invite':
        print('群邀请请求')
        try:
            flag=data['flag']
        except:
            print('获取invite失败')
        else:
            print('已同意邀请 进群请求')
            setGroupAddRequest(flag,'invite',True,'')

    try:
        request_type=data['request_type']
    except:
        request_type=None
    if request_type=='friend':
        try:
            flag=data['flag']
            qq=data['user_id']
        except:
            print('获取加好友flag失败')
        else:
            setFriendAddRequest(flag,True,None)
            sendPrivateMsg(qq,'添加好友成功，快回复"菜单"试试有什么功能吧!')



    # result=bot.get_group_list()
    # print('result=',result)
    return HttpResponse('true')


menu_list={
    '01':'短连接转换',
    '02':'二维码生成',
    '03':'图片转文字',
    '04':'文字转图片',
    '05':'文字转语音',
    '06':'带壳截图'
}
fun_list={
    '01':'shortUrl',
    '02':'codeMake',
    '03':'ocr',
    '04':'wordToImg',
    '05':'wordToVoice',
    '06':'shellScreen'
}

#菜单
def menu(**info):
    if info['msg'] in ['菜单','功能']:
        try:
            status = UserStatus.objects.get(qq=info['qq']).status
        except UserStatus.DoesNotExist:
            status = '0'
        if status == '0':
            menuText = ''
            menuText += '----菜单----\n'
            keys = list(menu_list.keys())
            keys.sort()
            print(keys)
            for key in keys:
                menuText += '%s.%s\n' % (key, menu_list[key])
            menuText += '------------\n'
            menuText += '回复序号使用相应功能\n'
            menuText += '更多功能正在开发中...'
            sendPrivateMsg(info['qq'], menuText)
        else:
            pass



def keyHandle(**info):
    try:
        status = UserStatus.objects.get(qq=info['qq']).status
    except UserStatus.DoesNotExist:
        status='0'
    info['status']=status
    print('status=',status)
    if status=='0':
        if info['msg'].isdigit():
            print('回复为数字')
            num = info['msg']
            print('num=%s' % num)
            try:
                globals().get(fun_list[num])(**info)  # 执行相应函数
            except:
                sendPrivateMsg(info['qq'], '口令不存在')
    else:
        globals().get(fun_list[status])(**info)



