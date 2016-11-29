import requests
import json

class Firebase:
    def __init__(self, token):
        self.myUrl = 'https://fcm.googleapis.com/fcm/send'
        self.payload = {
            "to": token,
            "notification": {}
        }

        self.headers = {
            'UserAgent': "FCM-Server",
            'Content-Type': 'application/json',
            'Authorization': "key=AAAAV-kOpiQ:APA91bF0nM7MJ70kCrFCaLEzncirYFigDT7_TGGZObSvecw9xJ4KBbpTVJwxUICV6ZDfv2XzIeI2H7-XBO1po8j8G-cLov5_xWAF0XF3t6xiLWuUGjQGynM3zluFsRNKIy4dpqCQCh600i04xvjXLu8TWhMLeNB5ZA"
        }

    def push(self, title, body):
        self.payload["notification"]['title'] = title
        self.payload["notification"]['text'] = body

        res = requests.post(self.myUrl, json.dumps(self.payload), headers=self.headers)

        return res.content