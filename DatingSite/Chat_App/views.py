from django.shortcuts import render
from django.contrib.auth.models import User
from friendship.models import Friend
from .models import messages
import json

def chathome(request):
    friendList = Friend.objects.friends(request.user)
    friendListwUnreadCount = {}
    for friend in friendList:
        friendListwUnreadCount[friend] = len(messages.objects.filter(sender=friend).filter(receiver=request.user).filter(read=False))
    return render(request, 'Chat_App/chathome.html', {'currUser': request.user,
                                                      'friendListwUnreadCount': friendListwUnreadCount})

def chatpage(request, withuser):
    withUser = User.objects.get(username=withuser)
    friendList = Friend.objects.friends(request.user)
    friendListwUnreadCount = {}
    for friend in friendList:
        friendListwUnreadCount[friend] = len(messages.objects.filter(sender=friend).filter(receiver=request.user).filter(read=False))
    
    if withUser.pk > request.user.pk:
        chatName = str(withUser.pk) + '_and_' + str(request.user.pk)
    else:
        chatName = str(request.user.pk) + '_and_' + str(withUser.pk)
        
    for msg in messages.objects.filter(sender=withUser).filter(receiver=request.user).filter(read=False):
        msg.read = True
        msg.save()
        
    prevmessagesSent = messages.objects.filter(sender=request.user).filter(receiver=withUser)
    prevmessagesFrom = messages.objects.filter(sender=withUser).filter(receiver=request.user)
    
    thisChat = list(prevmessagesFrom) + list(prevmessagesSent)
    thisChat.sort(key= lambda x: x.timeSent)
    thisChatList = []
    for i in thisChat: thisChatList.append({'sender': i.sender.username, 'receiver': i.receiver.username, 'content': i.content})
    thisChatJSON = json.dumps(thisChatList)

    return render(request, 'Chat_App/chatpage.html', {'currUser': request.user,
                                                      'withUser': withUser,
                                                      'friendListwUnreadCount': friendListwUnreadCount,
                                                      'chatName': chatName,
                                                      'thisChatJSON': thisChatJSON})