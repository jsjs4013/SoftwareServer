"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 model과 view사이의 연결통로 및 적절한 컨트롤러 역할을 한다.
 외래키의처리 데이터형식설정 create, update등 model과 view의 사이에서 적절한 다리역할을 한다.

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

import requests
import json

class Firebase:
    def __init__(self, token):
        self.myUrl = 'https://fcm.googleapis.com/fcm/send'
        self.payload = {
            "to": token,
            "time_to_live": 3,
            "notification": {
            }
        }

        self.headers = {
            'UserAgent': "FCM-Server",
            'Content-Type': 'application/json',
            'Authorization': "key=AAAAdmFKJrk:APA91bF7NujDfvLFOO0JG2u1InvEhY0hUd4ruZVVcPlekW-ldYboOzLYNq0stHts7mx-SQzKx-iqojXOX6M7jWegKv8eQkdGtYclsRFmyyjAndLz9PttqSed4UBxKAzQM_mSQ8QmfpmwDLoO1P9dKC5vMP8gq6bngg"
        }

    def push(self, title, username, bookTitle):
        self.payload["notification"]['title'] = title
        self.payload["notification"]['text'] =  username + '님이 ' + bookTitle + '을 구매요청하였습니다.'

        res = requests.post(self.myUrl, json.dumps(self.payload), headers=self.headers)
        res.close()