"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 Firebase 푸시메시지를 위한 파일이다.
 기본설정목록과 push해야할 내용을 가진 메서드를 가지고 있다.
"""

import requests
import json

class Firebase:
    def __init__(self, token):
        self.myUrl = 'https://fcm.googleapis.com/fcm/send'
        self.payload = {
            "to": token,
            "time_to_live": 0,
            'priority' : 'high',
            'icon' : 'myicon',
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

        return res.content