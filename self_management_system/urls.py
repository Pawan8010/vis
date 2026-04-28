from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.data_view, name='data'),

    path('bachat/', views.bachat_view, name='bachat'),
    path('pigmi/', views.pigmi_view, name='pigmi'),

    # 👇 FIXED HERE
    path('add-member/', views.AddMember.as_view(), name='add_member'),

    path('members/', views.view_members, name='view_members'),

    path('loan/', views.loanmanagement, name='loanmanagement'),
    path('add-loan/', views.add_loan, name='add_loan'),
    path('mark-paid/<int:loan_id>/', views.mark_paid, name='mark_paid'),

    path('reports/', views.reports, name='reports'),

    path('pigmi/add-member/', views.add_pigmi_member, name='pigmi_add_member'),
    path('pigmi/members/', views.view_pigmi_members, name='pigmi_view_members'),
    path('pigmi/dashboard/', views.pigmi_dashboard, name='pigmi_dashboard'),

    path('pigmi/deposit/', views.add_pigmi_collection, name='pigmi_deposit'),
    path('pigmi/withdraw/<int:member_id>/', views.withdraw_pigmi, name='pigmi_withdraw'),
    path('pigmi/member/<int:member_id>/', views.pigmi_member_detail, name='pigmi_member_detail'),
]