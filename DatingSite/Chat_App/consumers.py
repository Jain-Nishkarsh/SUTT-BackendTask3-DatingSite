import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import messages
from asgiref.sync import sync_to_async
# import websockets.client as websockets

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


class UserSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiverID = self.scope["url_route"]["kwargs"]["userID"]
        self.groupName = "chat_%s" % self.receiverID
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
        self.senderID = text_data_json["senderID"]
        
        await createMessage(await getUserpk(self.senderID), await getUserpk(self.receiverID), message)
        
        await self.channel_layer.group_send(
            self.groupName, 
            {
                "type": "chatbox_message",
                "message": message,
                "senderID": self.senderID,
            }
        )
    
    async def chatbox_message(self, event):
        message = event["message"]
        senderID = event["senderID"]
        
        await self.send(text_data=json.dumps(
            {"message":message, 
             "senderID":senderID,}))
    
    pass