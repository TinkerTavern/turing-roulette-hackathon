import requests; # requests library to make REST calls
import json


class mitsukuBot():

    def __init__(self):
        self.url = "https://miapi.pandorabots.com/talk"
        self.msg = ""
        self.headers = {'Content-type' : 'application/x-www-form-urlencoded', 'Referer': 'https://www.pandorabots.com/mitsuku/'};


    def sendMessage(self, msg):
        self.msg = msg
        self.data = {"input": msg
                    ,"sessionid": "403717205"
                    ,"channel": "6"
                    ,"botkey": "n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~"
                    ,"client_name": "cw16e77bebb2d"}

        return self.recieveMessages()

    def recieveMessages(self):
        r=requests.post(self.url,headers=self.headers, data = self.data); # requests.post to make a post call to dummy server.
        #print (r.content)
        my_json = r.content.decode('utf8').replace("'", '"')
        #
        #print('- ' * 20)

        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)

        if data['status'] == "ok":
            arr = []
            for item in data['responses']:
                arr.append(json.dumps(item).replace("\""," ").replace("\'"," "))
            return arr[0]
        else:
            return ""
