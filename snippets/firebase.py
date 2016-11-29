import requests
import json

class Firebase:
    def __init__(self, token):
        self.myUrl = 'https://fcm.googleapis.com/fcm/send'
        self.payload = {
            "collapse_key" : token,
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

    def push(self, title, body):
        self.payload["notification"]['title'] = title
        self.payload["notification"]['text'] = body

        res = requests.post(self.myUrl, json.dumps(self.payload), headers=self.headers)

        return res.content