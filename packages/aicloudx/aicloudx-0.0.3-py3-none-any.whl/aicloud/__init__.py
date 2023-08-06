import os
import http.client, urllib.parse
import json
import requests


name = "aicloud"

__isInCloud=False
__mybucket=''
__pubbucket=''


def modelName(name):
    '''
    传入model名，返回在云上保存的模型名，如果在云外部调用，原值返回
    '''
    if __isInCloud == False:
        return name
    tmp=name.split('/')
    ret = os.path.join(__mybucket,'models',tmp[-1])
    return 's3://'+ret


def __init__():
    global __isInCloud
    global __mybucket
    global __pubbucket
    __isInCloud='AICLOUD' in os.environ
    if __isInCloud == False:
        return

    if 'MyBucket' in os.environ:
        __mybucket=os.environ['MyBucket']
    else:
        raise Exception('没有获取到有效环境变量MyBucket')

    if 'PublicBk' in os.environ:
        __pubbucket=os.environ['PublicBk']
    else:
        raise Exception('没有获取到有效环境变量PublicBk')



__init__()
if __name__=='__main__':
    __init__()
    a=modelName("abc/ab")
    print(a)