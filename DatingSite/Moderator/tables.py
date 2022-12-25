from .models import ReportUser
from django.contrib.auth.models import User
import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html


class ReportedTable(tables.Table):
    
    Actions = tables.TemplateColumn(template_code='<div style="display: flex; column-gap: 10px;">' + 
                                    '<a href="{% url \'Moderator:userAdminPage\' record.reportee.username %}" class="btn btn-danger" style="height: 1.5rem; display: flex; align-items: center;" >Ban User</a>'+
                                    '<a href="{% url \'Moderator:ignoreReport\' record.id %}" class="btn btn-outline-dark" style="height: 1.5rem; display: flex; align-items: center;" >Ignore</a></div>')
    
    class Meta:
        model = ReportUser
        template_name = "django_tables2/bootstrap4.html"
    
    def render_reporter(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('profile', kwargs={'username':record.reporter.username}),
                           record.reporter.username)
        
    def render_reportee(self, record):
        return format_html('<a href="{}">{}</a>',
                           reverse('profile', kwargs={'username':record.reportee.username}),
                           record.reportee.username)
    
    
class AllUserTable(tables.Table):
    
    Action = tables.TemplateColumn(template_code='<a href="{% url \'Moderator:userAdminPage\' record.username %}" class="btn btn-light" style="height: 1.5rem; display: flex; align-items: center;">Go to Profile</a>')
    
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = {'id','username', 'first_name', 'last_name', 'email', 'is_active', 'last_login'}
        sequence = ('id','username', 'first_name', 'last_name', 'email', 'is_active', 'last_login',)