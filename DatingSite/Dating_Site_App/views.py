from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import datetime

def age(DOB):
    return (datetime.datetime.now().date().year - DOB.year)

def editProfile(request, username):
    if request.user.username != username:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == "POST":
        userProfile = get_object_or_404(User, username=request.user)
        userProfile.username = request.POST.get('username')
        userProfile.first_name = request.POST.get('first_name')
        userProfile.last_name = request.POST.get('last_name')
        userProfile.profile.gender = request.POST.get('gender')
        userProfile.profile.DOB = request.POST.get('DOB')
        userProfile.profile.status = request.POST.get('status')
        userProfile.profile.bio = request.POST.get('bio')
        
        if 'profilephoto' in request.FILES.keys():
            upload = request.FILES['profilephoto']
            fileName = f'{userProfile.username}_profilePic.jpg'
            fss = FileSystemStorage()
            if fss.exists(fileName):
                fss.delete(fileName)
            file = fss.save(fileName, upload)
            file_url = fss.url(file)
            userProfile.profile.profilephoto = file_url

        userProfile.save()
        return HttpResponseRedirect(reverse('profile', args=(userProfile.username,)))
    
    else:
        return render(request, 'Dating_Site_App/editProfile.html', {'user':request.user})


def profile(request, username):
    userProfile = get_object_or_404(User, username=username)
    return render(request, 'Dating_Site_App/Profile.html', {'user':userProfile,
                                                            'currUser':request.user})
    
def home(request):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse('login'))
    
    if (not(request.user.profile.gender)
        and not(request.user.profile.status)
        and not(request.user.profile.bio)
        and not(request.user.profile.DOB)):
        return HttpResponseRedirect(reverse('editpage', args=(request.user.username,)))
    
    filteredUsers = {}
    userFilters = request.POST.dict()
    prefgender = []
    prefstatus = []
    
    if request.method == 'GET':
        prefgender.append('M')
        userFilters['gender_male'] = True
        prefgender.append('F')
        userFilters['gender_female'] = True
        prefgender.append('Others')
        userFilters['gender_others'] = True
        prefstatus.append('single')
        userFilters['status_single'] = True
        prefstatus.append('committed')
        userFilters['status_committed'] = True
        age_from = 16
        userFilters['age_from'] = age_from
        age_to = 25
        userFilters['age_to'] = age_to
    
    if request.method == 'POST':
        
        age_from = int(request.POST.get('age_from') or 0)
        age_to = int(request.POST.get('age_to') or 0)
        
        if request.POST.get('gender_male'):
            prefgender.append('M')
        if request.POST.get('gender_female'):
            prefgender.append('F')
        if request.POST.get('gender_others'):
            prefgender.append('Others')
        if request.POST.get('status_single'):
            prefstatus.append('single')
        if request.POST.get('status_committed'):
            prefstatus.append('committed')
                
    for user in User.objects.all():
        if ((user.profile.gender in prefgender) 
            and age(user.profile.DOB) in range(age_from, age_to+1) 
            and (user.profile.status in prefstatus)
            and (user.username != request.user.username)):
            filteredUsers[user] = age(user.profile.DOB)
         
    sentfriendReqList = []
    for sentReq in Friend.objects.sent_requests(user=request.user): sentfriendReqList.append(sentReq.to_user)
        
    incomingRequests = []
    for req in (Friend.objects.unread_requests(user=request.user)): incomingRequests.append(req.from_user)
    for req in Friend.objects.unrejected_requests(request.user): incomingRequests.append(req.from_user)
        
    return render(request, 'Dating_Site_App/home.html', {'currUser':request.user,
                                                         'userFilters':userFilters,
                                                         'filteredUsers': filteredUsers,
                                                         'friendList': Friend.objects.friends(request.user),
                                                         'sentfriendReqList': sentfriendReqList,
                                                         'incomingRequests':incomingRequests,})

def sendMessageRequest(request, touser):
    other_user = User.objects.get(username=touser)
    Friend.objects.add_friend(from_user=request.user,to_user=other_user)
    return HttpResponseRedirect(reverse('home'))

def respondMessageRequest(request, fromuser, response):
    from_user = User.objects.get(username=fromuser)
    friend_request = FriendshipRequest.objects.get(from_user=from_user, to_user=request.user)
    if (response == 'accept'):
        friend_request.accept()
    elif (response == 'reject'):
        friend_request.reject()
        friend_request.cancel()
        
    return HttpResponseRedirect(reverse('messagerequestspage'))


def messageRequests(request):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse('login'))
    
    # unreadRequests = []
    # for req in Friend.objects.unread_requests(request.user):
    #     unreadRequests.append([req.from_user, age(req.from_user.profile.DOB)])
    #     FriendshipRequest.objects.get(from_user=req.from_user, to_user=request.user).mark_viewed()
        
    ignoredRequests = []
    for req in Friend.objects.unrejected_requests(request.user):
        ignoredRequests.append([req.from_user, age(req.from_user.profile.DOB)])

    return render(request, 'Dating_Site_App/messageRequestsPage.html', {'currUser':request.user,
                                                                        # 'unreadRequests': unreadRequests,
                                                                        # 'unreadRequestscount': Friend.objects.unread_request_count(request.user),
                                                                        'ignoredRequests': ignoredRequests,
                                                                        'ignoredRequestscount':Friend.objects.unrejected_request_count(request.user),})
    

def blockUser(request, touser):
    other_user = User.objects.get(username=touser)
    Block.objects.add_block(request.user, other_user)
    return HttpResponseRedirect(reverse('profile', args=(touser)))