from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block
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
         
           
        # if ((not(request.POST.get('gender_male')))
        #     and (not(request.POST.get('gender_female')))
        #     and (not(request.POST.get('gender_others')))
        #     and (not(request.POST.get('status_single')))
        #     and (not(request.POST.get('status_committed')))
        #     and (not(request.POST.get('age_from')))
        #     and (not(request.POST.get('age_to')))):
        #     prefgender.append('M')
        #     userFilters['gender_male'] = True
        #     prefgender.append('F')
        #     userFilters['gender_female'] = True
        #     prefgender.append('Others')
        #     userFilters['gender_others'] = True
        #     prefstatus.append('single')
        #     userFilters['status_single'] = True
        #     prefstatus.append('committed')
        #     userFilters['status_committed'] = True
        #     age_from = 16
        #     userFilters['age_from'] = age_from
        #     age_to = 25
        #     userFilters['age_to'] = age_to
            
    for user in User.objects.all():
        if ((user.profile.gender in prefgender) 
            and age(user.profile.DOB) in range(age_from, age_to+1) 
            and (user.profile.status in prefstatus)
            and (user.username != request.user.username)):
            filteredUsers[user] = age(user.profile.DOB)
                
    for friend in (Friend.objects.friends(request.user)):
        print(friend)
                
    # print((Friend.objects.sent_requests(user=request.user)[0].to_user))
    sentfriendReqList = []
    for sentReq in (Friend.objects.sent_requests(user=request.user)):
        sentfriendReqList.append(sentReq.to_user)
        
    return render(request, 'Dating_Site_App/home.html', {'currUser':request.user,
                                                         'userFilters':userFilters,
                                                         'filteredUsers': filteredUsers,
                                                        #  'friendList': friendList,
                                                         'sentfriendReqList': sentfriendReqList,})

def sendMessageRequest(request, touser):
    print('----')
    other_user = User.objects.get(username=touser)
    Friend.objects.add_friend(request.user, other_user)
    return HttpResponseRedirect(reverse('home'))

