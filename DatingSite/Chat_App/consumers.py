import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import messages
from asgiref.sync import sync_to_async

@sync_to_async
def getUserpk(i):
    return User.objects.get(pk = i)

@sync_to_async
def getUserusername(name):
    return User.objects.get(username=name)

@sync_to_async
def createMessage(sender, receiver, content):
    msg = messages.objects.create(sender=sender, receiver=receiver, content=content)
    msg.save()
    
@sync_to_async
def getMessages(sender, receiver):
    msgList = []
    # print('------')
    # print(messages.objects.filter(sender=sender, receiver=receiver))
    # print('------')
    return list(
        messages.objects.filter(sender=sender, receiver=receiver)
    )
    # for i in messages.objects.filter(sender=sender, receiver=receiver):
    #     msgList.append(i)
    # return msgList

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatboxName = self.scope["url_route"]["kwargs"]["withuser"]
        self.groupName = "chat_%s" % self.chatboxName
        await self.channel_layer.group_add(
            self.groupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        
        for i in self.scope["url_route"]["kwargs"]["withuser"].split('_and_'):
            if (await getUserpk(i)) != (await getUserusername(username)):
                toUser = (await getUserpk(i))
        
        await createMessage(await getUserusername(username), toUser, message)
        
        # db.get('id').messages = json.dumps(json.loads(messages) + [text_data_json])
        
        await self.channel_layer.group_send(
            self.groupName, 
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            }
        )
        
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps(
            {"message":message, 
             "username":username,}))
    
    pass