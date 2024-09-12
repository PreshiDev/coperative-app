from django.urls import path

from .views import (member,member_detail,
                   member_create, user_login, MemberAccountRegister, MemberDashboardView, logout_view, Dashboard,
                   send_message, inbox, view_message, member_inbox, MemberAccountEditView,
                   StaffAccountEditView, AddStaffMemberView, unread_notifications_count, mark_notifications_as_read)

app_name = 'members'
urlpatterns = [
        path('', user_login, name='login'),
        path('logout/', logout_view, name='logout'),
        path('members/', member, name='member'),
        path('signup/', MemberAccountRegister, name='signup'),
        path('create/', member_create, name='create'),
        #path('<str:mem_number>/', member_detail, name='member_detail'),
        path('member/<int:mem_number>/', member_detail, name='member_detail'),  # Member detail URL
        path('dashboard/', MemberDashboardView, name='dashboard'),  # Dashboard URL
        path('admin_dashboard/', Dashboard, name='admin_dashboard'),  # Dashboard URL
        path('send/', send_message, name='send_message'),
        path('inbox/', inbox, name='inbox'),
        path('message/<int:message_id>/', view_message, name='view_message'),
        path('member-inbox/', member_inbox, name='member_inbox'),
        path('edit-account/', MemberAccountEditView, name='edit_account'),
        path('staff/edit-account/', StaffAccountEditView, name='staff_edit_account'),
        path('staff/add/', AddStaffMemberView, name='add_staff_member'),
        path('admin_dashboard/', member, name='admin_dashboard'),
         # URL for fetching unread notifications count
        path('unread_notifications_count/', unread_notifications_count, name='unread_notifications_count'),
        
        # URL for marking notifications as read
        path('mark_notifications_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),
]
