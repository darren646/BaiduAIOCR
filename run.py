

"""
百度AI开放平台链接：https://ai.baidu.com/
图片识别API文档链接：https://ai.baidu.com/docs#/OCR-API-GeneralBasic/db0895e7
应用注册链接：https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list

"""

#coding=utf-8
__author__ = 'darrenyan'
__date__ = '2020/05/10 13:30'
import requests
import json
import base64
import time
import re


class baiduCode(object):

    @classmethod
    def get_token(cls):
        """
        当前函数只用调用一次，用来获取当前账号的token
        :return:
        """
        # 标记当前精准识别是否使用完
        cls.curr_url = ''
        cls.basic_flag = False
        cls.max_num = 5
        cls.login_url = 'https://aip.baidubce.com/oauth/2.0/token'
        #client_id,client_secret在百度ai上建立应用后会分配
        cls.login_params = {
            'grant_type': 'client_credentials',
            'client_id': 'OLVtun8wprg1G1tPQoZjeYDK',
            'client_secret': 'vR3lQNVnn6R0003NVlTOH7jv54DRtbDt'
        }
        cls.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(cls.login_url, params=cls.login_params, headers=cls.headers)
        result = json.loads(response.text)
        cls.token = result['access_token']

    @classmethod
    def get_code(cls, path='', url=''):
        dsturl=url
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        m=re.match(regex, dsturl)
        if(m!=None):
            rpicture = requests.get(url=dsturl)
            with open("picture.jpeg", "wb+") as f:
                f.write(rpicture.content)

        print(re.match(regex, dsturl) is not None)  # True





        cls.num = 0
        # 普通图片识别的请求链接，正确率50%（测试了500张图片）//url方式使用
        cls.general_basic_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        # 高精度图片识别的请求链接，正确率80%（测试了500张图片）
        cls.accurate_basic_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
        if path:
            if not cls.basic_flag:
                cls.curr_url = cls.accurate_basic_url
            with open(path, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                base = base64_data.decode()
                cls.basic_params = {
                    'image': base,
                    'access_token': cls.token
                }
        elif url:
            cls.curr_url = cls.general_basic_url
            cls.basic_params = {
                'url': url,
                'access_token': cls.token
            }
        else:
            raise ValueError('当前path和url参数均错误')
        time.sleep(0.5)
        while True:
            try:
                response = requests.post(cls.curr_url, params=cls.basic_params, headers=cls.headers)
                result = json.loads(response.text)
                # 判断当前精准识别是否被使用完
                try:
                    result['words_result']
                except Exception as e:
                    print(e)
                    cls.num += 1
                    if cls.num > cls.max_num:
                        raise ValueError('当前尝试的错误次数超过%d次，请重新调用'%(cls.max_num))
                    cls.basic_flag = True
                    cls.curr_url = cls.general_basic_url
                    continue
                code = result['words_result'][0]['words']
                return code
                break
            except Exception as e:
                print('error: ', e)
                cls.num += 1
                if cls.num > cls.max_num:
                    raise ValueError('当前尝试的错误次数超过%d次，请重新调用'%(cls.max_num))


if __name__ == '__main__':
    # 当前获取token的函数只用调用一次
    baiduCode.get_token()
    # 直接传图片的地址就好
    code = baiduCode.get_code(path=r'D:\Onebox\Codes\Python\BaiduAIOCR\picturea.jpeg')
    print(code)
    # code = baiduCode.get_code(url='https://www.showapi.com/auth/checkCode?t=1571279918029')
    # print(code)
    pass
