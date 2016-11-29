import requests
import json

class Firebase:
    def __init__(self, token):
        self.myUrl = 'https://fcm.googleapis.com/fcm/send'
        self.payload = {
            "collapse_key" : token,
            "to": token,
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