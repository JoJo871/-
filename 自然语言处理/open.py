"""
@author: HeroZhang（池塘春草梦）
@contact:herozhang101@gmail.com
@version: 1.0.0
@file: law_ques.py
@time: 2024/1/11 16:25
@description: 调用文心一言api,实现批量回答问题
"""

import json

import pandas as pd
import requests
from tqdm import tqdm

API_KEY = "EtjoZonRPIFTpUVMTNdXYOkt"
SECRET_KEY = "PP3laMZJdAtvQtJxfJbFpmxmSl4ZhcEU"

def ask_Q(question):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


questions = [
    "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。","你认为这款智能手表对用户的健康管理是否有重要意义？"
    # 在这里添加更多问题
]

answers = []

for question in questions:
    answer = ask_Q(question)
    answers.append(answer['result'])

# 输出答案
for question, answer in zip(questions, answers):
    print("问题:", question)
    print("答案:", answer)
    print()

