from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ReportUser
from .tables import ReportedTable, AllUserTable
from django.contrib.auth.models import User

def modHome(request):
    if (request.user.is_authenticated != True):
        return HttpResponseRedirect(reverse('login'))
    
    if (request.user not in User.objects.filter(is_superuser=True)):
        return HttpResponseRedirect(reverse('login'))
    
    querySetReport = ReportUser.objects.all()
    Reporttable = ReportedTable(querySetReport)
    
    querySetAll = User.objects.all()
    AllUsersTable = AllUserTable(querySetAll)
    
    return render(request, 'Moderator/modHome.html', {'currUser': request.user,
                                                      'reportedCount': len(ReportUser.objects.all()),
                                                      'reportTable': Reporttable,
                                                      'registeredCount': len(User.objects.all()),
                                                      'allUsersTable': AllUsersTable})
    
    
def redirectAdminUser(request, reportee):
    reporteeUser = User.objects.get(username=reportee)
    return HttpResponseRedirect(reverse('admin:auth_user_change', args=(reporteeUser.id,)))


def ignoreReport(request, reportID):
    report = ReportUser.objects.get(id=reportID)
    report.delete()
    return redirect('Moderator:modhome')