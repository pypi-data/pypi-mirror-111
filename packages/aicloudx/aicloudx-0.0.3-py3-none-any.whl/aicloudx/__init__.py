import os
import http.client, urllib.parse
from posixpath import join
import json
import requests
from minio import Minio
from minio.error import S3Error

name = "aicloudx"

__isInCloud=False
__mybucket=''
__pubbucket=''


def modelName(name:str):
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
    __isInCloud='MyBucket' in os.environ
    if __isInCloud == False:
        return

    __mybucket=os.environ['MyBucket']

    if 'PublicBk' in os.environ:
        __pubbucket=os.environ['PublicBk']
    else:
        raise Exception('没有获取到有效环境变量PublicBk')

def load(name:str, data_dir:str=None):
    '''load(name [, data_dir=None])

    下载数据，name要下载的数据名字，data_dir为存储目录，默认为~/tensorflow_datasets/
    '''
    bucket = 'tfdatasets'
    data_prefix = os.path.join('tensorflow_datasets',name)
    if not data_dir:
        data_dir = os.path.join(os.environ['HOME'],data_prefix)
    else:
        data_dir = os.path.join(data_dir, name)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    # client = Minio(
    #     "localhost:9000",
    #     access_key="abcd",
    #     secret_key="79cfeb94595de33b3326c06ab1c7dbda",
    #     secure=False)
    client = Minio(
        os.environ['S3_ENDPOINT'],
        secure=False)
    objects = client.list_objects(
        bucket, prefix=data_prefix, recursive=True,
    )
    length = len(data_prefix)
    for obj in objects:
        tmp=os.path.join(data_dir,obj.object_name[length+1:])
        if obj.is_dir:
            if not os.path.isdir(tmp):
                os.makedirs(tmp)
        client.fget_object(bucket, obj.object_name, tmp)

__init__()
if __name__=='__main__':
    a=modelName("abc/ab")
    print(a)
    load('mnist','./dataxx')