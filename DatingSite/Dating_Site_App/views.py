from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from friendship.models import Friend, Block, FriendshipRequest
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import datetime
from Moderator.models import ReportUser
from django.contrib.auth import authenticate, login
from fuzzywuzzy import fuzz

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

def modLogin(request):
    
    if request.POST['username'] and request.POST['password']:
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            if not User.objects.get(username=username).is_superuser:
                return HttpResponseRedirect(reverse('home'))

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Moderator:modhome'))
        except:
            return HttpResponseRedirect(reverse('home'))
    
    return HttpResponseRedirect(reverse('home'))

def profile(request, username):
    userProfile = get_object_or_404(User, username=username)
    blocked = Block.objects.is_blocked(request.user, userProfile)
    friends = Friend.objects.are_friends(request.user, userProfile)
    reported = (len(list(ReportUser.objects.filter(reporter=request.user, reportee=userProfile))) > 0)
    
    sentfriendReqList = []
    for sentReq in Friend.objects.sent_requests(user=request.user): sentfriendReqList.append(sentReq.to_user)
    
    return render(request, 'Dating_Site_App/Profile.html', {'user':userProfile,
                                                            'currUser':request.user,
                                                            'blocked':blocked,
                                                            'friends':friends,
                                                            'sentfriendReqList':sentfriendReqList,
                                                            'reported': reported})
    
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
        fuzzCondition = True
        if request.POST.get('searchBox'):
            fuzzScoreUsername = fuzz.token_set_ratio(request.POST.get('searchBox'), user.username)
            fuzzScoreFullname = fuzz.token_set_ratio(request.POST.get('searchBox'), user.get_full_name)
            fuzzCondition = (max(fuzzScoreUsername, fuzzScoreFullname) > 69)
        
        if ((user.profile.gender in prefgender) 
            and age(user.profile.DOB) in range(age_from, age_to+1) 
            and (user.profile.status in prefstatus)
            and (user.username != request.user.username)
            and not Block.objects.is_blocked(request.user, user)
            and (fuzzCondition)):
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
    return redirect(request.META.get('HTTP_REFERER'))

def unsendMessageRequest(request, touser):
    other_user = User.objects.get(username=touser)
    friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
    friend_request.cancel()
    return redirect(request.META.get('HTTP_REFERER'))

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
      
    ignoredRequests = []
    for req in Friend.objects.unrejected_requests(request.user):
        ignoredRequests.append([req.from_user, age(req.from_user.profile.DOB)])

    return render(request, 'Dating_Site_App/messageRequestsPage.html', {'currUser':request.user,
                                                                        'ignoredRequests': ignoredRequests,
                                                                        'ignoredRequestscount':Friend.objects.unrejected_request_count(request.user),})
    
def blockUser(request, touser):
    other_user = User.objects.get(username=touser)
    Block.objects.add_block(request.user, other_user)
    Friend.objects.remove_friend(request.user, other_user)
    return HttpResponseRedirect(reverse('profile', args=(other_user.username,)))

def unblockUser(request, touser):
    other_user = User.objects.get(username=touser)
    Block.objects.remove_block(request.user, other_user)
    return redirect(request.META.get('HTTP_REFERER'))

def Unmatch(request, touser):
    other_user = User.objects.get(username=touser)
    Friend.objects.remove_friend(request.user, other_user)
    return HttpResponseRedirect(reverse('home'))

def blocklist(request):
    blockList = {}
    for user in Block.objects.blocking(request.user):
        blockList[user] = age(user.profile.DOB)
        
    return render(request, 'Dating_Site_App/blocklist.html', {'currUser':request.user,
                                                              'blockedUsers': blockList,
                                                              'blockedUsersCount': len(Block.objects.blocking(request.user))})
    
def allmatches(request):
    friendList = {}
    for user in Friend.objects.friends(request.user):
        friendList[user] = age(user.profile.DOB)
        
    return render(request, 'Dating_Site_App/allMatches.html', {'currUser':request.user,
                                                              'friendList': friendList,
                                                              'friendsCount': len(Friend.objects.friends(request.user))})
        
def Report(request, reportee):
    reporteeUser = User.objects.get(username = reportee)
    # if reporteeUser not in Follow.objects.following(request.user):
    #     Follow.objects.add_follower(request.user, reporteeUser)
    if not ReportUser.objects.filter(reporter=request.user, reportee=reporteeUser):
        report = ReportUser.objects.create(reporter=request.user, reportee=reporteeUser, reportMessage=request.POST.get('reportMessage'))
        report.save()
        
    if not Friend.objects.are_friends(request.user, reporteeUser):
        Friend.objects.remove_friend(request.user, reporteeUser)
    if not Block.objects.is_blocked(request.user, reporteeUser):
        Block.objects.add_block(request.user, reporteeUser)
    if reporteeUser in Friend.objects.unrejected_requests(request.user):
        friend_request = FriendshipRequest.objects.get(from_user=reporteeUser, to_user=request.user)
        friend_request.cancel()
        
    return HttpResponseRedirect(reverse('profile', args=(reporteeUser.username,)))

def ReportPage(request, reportee):
    reporteeUser = User.objects.get(username=reportee)
    return render(request, 'Dating_Site_App/ReportPage.html', {'currUser': request.user,
                                                               'reportee': reporteeUser})